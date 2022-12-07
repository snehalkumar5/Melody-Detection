#include <bits/stdc++.h>
using namespace std;
int minCollectingSpeed(vector<int>& piles,
					int H)
{
	int ans = -1;
	int low = 1, high;
	high = *max_element(piles.begin(),
						piles.end());
	while (low <= high)
	{
		int K = low + (high - low) / 2;
		int time = 0;
		for (int ai : piles) {
			time += (ai + K - 1) / K;
		}
		if (time <= H) {
			ans = K;
			high = K - 1;
		}
		else {
			low = K + 1;
		}
	}
	cout << ans;
}
int main()
{
	vector<int> arr = { 3, 6, 7, 11 };
	int H = 8;
	minCollectingSpeed(arr, H);
	return 0;
}
