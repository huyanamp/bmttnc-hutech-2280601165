#Nhập số từ người dùng
so = int(input("Nhap mot so nguyen: "))
#Kiểm tra xem số đó có phải số chẵn hay không
if so % 2 == 0:
    print(so, "la so chan.")
else:
    print(so, "khong phai la so chan.")