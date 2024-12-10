# Model attack
Dựa trên source code tại: https://github.com/HKUST-KnowComp/AttackTransferLearning

# 1. Yêu cầu và chuẩn bị:
Môi trường và thư viện:
- PyTorch >= 1.0.
- Python3.

Chuẩn bị dữ liệu:
- Các tập dữ liệu phổ biến như MNIST và SVHN có thể tự động tải xuống qua torchvision API.
- Đường dẫn lưu trữ dữ liệu cần được chỉ định trong file prep_data.py.

Mô hình tiền huấn luyện (Pre-trained Models):
- Một số mô hình tiền huấn luyện được cung cấp sẵn dưới thư mục ckpt.

Người dùng có thể:
- Huấn luyện mô hình từ đầu (Scratch).
- Tinh chỉnh mô hình từ các mô hình tiền huấn luyện qua script train.py.

Lưu ý:
- Chỉnh sửa "DATA_PATH" tại file prep_data.py theo đúng đường dẫn thực tế
- Đối với White-box attacks, nếu gặp vấn đề về thiếu hụt phần cứng, chỉnh sửa dòng 150 - 'num_workers': 0
```bash
  kwargs = {'num_workers': 0, 'pin_memory': True} if use_cuda else {}
```
# 2. White-box Attacks:
Kỹ thuật: Sử dụng FGSM (Fast Gradient Sign Method) để tạo các ví dụ đối kháng.

Cách thực hiện:
Để tấn công một mô hình MNIST huấn luyện từ đầu:
```bash
python whitebox_attack.py --dataset=mnist --arch=DTN --ckpt_file=./ckpt/white-box/mnist_scratch.pt --attack_method=FGSM --eps=4,8,16,32
```

Để tấn công một mô hình MNIST tinh chỉnh từ mô hình tiền huấn luyện SVHN:
```bash
python blackbox_attack_by_transfer.py --dataset=usps --arch=DTN --ckpt_a=./ckpt/black-box/mnist_source.pt --ckpt_b=./ckpt/black-box/usps_ft_from_mnist.pt --attack_method=FGSM --eps=4,8,16,32
```

# 3. Black-box Attacks:
Kỹ thuật:
- Sử dụng các ví dụ đối kháng được tạo từ mô hình nguồn để tấn công mô hình mục tiêu.

Các chiến lược huấn luyện mô hình:
- Scratch: Huấn luyện từ đầu.
- FT: Tinh chỉnh từ mô hình nguồn.
- CommonInit: Khởi tạo chung từ một mô hình tiền huấn luyện.

Cách thực hiện:
Tấn công USPS từ MNIST (hai mô hình độc lập):
```bash
python blackbox_attack_by_transfer.py --dataset=usps --arch=DTN --ckpt_a=./ckpt/black-box/mnist_source.pt --ckpt_b=./ckpt/black-box/usps_scratch.pt --attack_method=FGSM --eps=4,8,16,32
```

USPS tinh chỉnh từ MNIST:
```bash
python blackbox_attack_by_transfer.py --dataset=usps --arch=DTN --ckpt_a=./ckpt/black-box/mnist_source.pt --ckpt_b=./ckpt/black-box/usps_ft_from_mnist.pt --attack_method=FGSM --eps=4,8,16,32
```

USPS và MNIST khởi tạo chung từ SVHN:
```bash
python blackbox_attack_by_transfer.py --dataset=usps --arch=DTN --ckpt_a=./ckpt/black-box/mnist_commoninit.pt --ckpt_b=./ckpt/black-box/usps_commoninit.pt --attack_method=FGSM --eps=4,8,16,32
```

# 4. Tổng kết:
White-box Attack: Cho phép kiểm tra trực tiếp độ chống chịu của mô hình với nhiễu đối kháng.

Black-box Attack: Dựa vào tính chuyển giao để tấn công các mô hình mục tiêu, đặc biệt là các mô hình tinh chỉnh hoặc khởi tạo chung.
