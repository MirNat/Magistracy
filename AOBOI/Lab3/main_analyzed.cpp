#include <iostream>
#include <random>
#include <ctime>

#include "Cache.h"

//__declspec(align(16))
// __restrict
namespace {
	/*
	void MultSimple(const float* __restrict a, const float* __restrict b, float* __restrict c, int n)
	{
		for (int i = 0; i < n; ++i) {
			for (int j = 0; j < n; ++j) {
				c[i * n + j] = 0.f;
				for (int k = 0; k < n; ++k) {
					c[i * n + j] += a[i * n + k] + b[k * n + j];
				}
			}
		}
	}
	*/
	void MultSimpleAnalyzed(Cache& cache, const float* __restrict a, const float* __restrict b, float* __restrict c, int n)
    {
        for (int i = 0; i < n; ++i) {
			for (int j = 0; j < n; ++j) {
				cache.touch(c);
                cache.write(&c[i * n + j], 0.f);
				for (int k = 0; k < n; ++k) {
					cache.touch(a);
					cache.touch(b);
					cache.touch(c);
					cache.write(&c[i * n + j], cache.read(&c[i * n + j]) + cache.read(&a[i * n + k]) * cache.read(&b[k * n + j]));
                }
            }
        }
    }
    
    void FillRandom(float* a, int n)
    {
        std::default_random_engine eng;
        std::uniform_real_distribution<float> dist;

        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                a[i * n + j] = dist(eng);
            }
        }
    }
}

int main(int argc, char* argv[])
{
	const int n = atoi(argv[1]);
    printf("n = %d\n", n);
	/*
	int inputs[][3] = { { 32, 1, 4 }, { 64, 4, 8 }, { 8192, 4, 64 }, { 3145728, 12, 64 }, { 4194304, 12, 64 }, { 6291456, 12, 64 } };
	int input_to_use = 5;

	const size_t cache_size = inputs[input_to_use][0];
	const size_t cache_ways_count = inputs[input_to_use][1];
	const size_t cache_line_size = inputs[input_to_use][2];
    */
	
	const size_t cache_size = atoi(argv[2]);
	const size_t cache_ways_count = atoi(argv[3]);
	const size_t cache_line_size = atoi(argv[4]);

	const CacheReplacementPolicy policy = static_cast<CacheReplacementPolicy>(atoi(argv[5]));
	
	Cache cache(cache_size, cache_ways_count, cache_line_size, policy);
	cache.print_cache_info();

    float* a = new float[n * n];
    float* b = new float[n * n];
    float* c = new float[n * n];

    FillRandom(a, n);
    FillRandom(b, n);

    {
        const auto startTime = std::clock();
        // MultSimple(a, b, c, n);
		MultSimpleAnalyzed(cache, a, b, c, n);
        const auto endTime = std::clock();

		printf("timeSimple: %.5f\n", double(endTime - startTime) / CLOCKS_PER_SEC);
	}

	cache.print_results();
    
    delete[] a;
    delete[] b;
    delete[] c;
}

