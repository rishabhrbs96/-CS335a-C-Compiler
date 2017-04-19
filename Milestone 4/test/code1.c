int main(){
	int a = 0;
	int b = 1;
	int result = 0;
	for(int t = 2; t <= 10; t++) {
		result = a + b;
		a = b;
		b = result;
	}
}