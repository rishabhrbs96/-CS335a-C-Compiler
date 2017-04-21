int a = 3;
int b[2][2];
int main(){
	int d = 2147483647;
	int bss = 1;
	b[1][1] = d;
	b[1][0] = bss;
	int result = b[1][1] * b[1][0];
}