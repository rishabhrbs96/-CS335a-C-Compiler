int main(){
	int a = 0;
	int b = 1;
	int t = 2;
	int result = 0;
	while(t <= 10) {
		result = a + b;
		a = b;
		b = result;
		t = t + 1;
	}
}