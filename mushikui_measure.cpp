#include <iostream>
#include <chrono>
using namespace std;

// 100~999の数のペアを全探索
void f1(){
	int x[900];
	for( int i = 0; i < 900; i++ )
	{
		x[i] = i+100;
	}

	for( int i = 0; i < 900; i++ )
	{
		for( int j = 0; j < 900; j++ )
		{
			int a = x[i], b = x[j];
			int a100 = a/100, a10 = a/10%10, a1 = a%10;
			int b100 = b/100, b10 = b/10%10, b1 = b%10;

			// 5が含まれない
			if( a100 == 5 || a10 == 5 || a1 == 5 || b100 == 5 || b10 == 5 || b1 == 5 ) continue;

			// 1段目
			if( a*b1 < 100 || a*b1 > 999 || (a*b1)/10%10 != 5 ) continue;

			// 2段目
			if( a*b10 < 100 || a*b10 > 999 ) continue;

			// 3段目
			if( a*b100 < 100 || a*b100 > 999 || (a*b100)/100 != 5 ) continue;

			// 4段目
			if( a*b < 55500 || a*b > 55599 ) continue;

			// printf("Answer: %d × %d = %d\n", a, b, a*b);
		}
	}
}

// 今回のアルゴリズムを用いたもの
void f2(){
	for( int i = 126; i <= 234; i++ )
	{
		if( i-(55499%i) <= 100 )
		{
			// n*m = 555xx（虫食い算の6段目を満たす）
			int n = i, m = 55599/i;

			// n*mで虫食い算を検証
			if( n >= 200 ) swap(n, m);
			int m100 = m/100, m10 = m/10%10, m1 = m%10;
			int d3 = n*m1, d4 = n*m10, d5 = n*m100; // 虫食い算の3,4,5段目の数
			int d3_100 = d3/100, d3_10 = d3/10%10, d3_1 = d3%10;
			int d4_100 = d4/100, d4_10 = d4/10%10, d4_1 = d4%10;
			int d5_100 = d5/100, d5_10 = d5/10%10, d5_1 = d5%10;
			if( d3_10 == 5 && d5_100 == 5 && d3_100 != 5 && d3_1 != 5 && d4_100 != 5 && d4_10 != 5 && d4_1 != 5 && d5_10 != 5 && d5_1 != 5 ) // 虫食い算の3,4,5段目を満たす
			{
				int n100 = n/100, n10 = n/10%10, n1 = n%10;
				if( n100 != 5 && n10 != 5 && n1 != 5 && m100 != 5 && m10 != 5 && m1 != 5 ) // 虫食い算の1,2段目を満たす
				{
					// printf("Answer: %d × %d = %d\n", n, m, n*m);
				}
			}
		}
	}
}

int main() {
	chrono::system_clock::time_point start,end;

	// 計測１
	start = std::chrono::system_clock::now();
	for( int i = 0; i < 1000; i++ )
	{
		f1();
	}
	end = std::chrono::system_clock::now();
	printf("全探索：%ld[ms]\n", chrono::duration_cast<chrono::milliseconds>(end-start).count());

	// 計測２
	start = std::chrono::system_clock::now();
	for( int i = 0; i < 1000; i++ )
	{
		f2();
	}
	end = std::chrono::system_clock::now();
	printf("今回のアルゴリズム：%ld[ms]\n", chrono::duration_cast<chrono::milliseconds>(end-start).count());
}
