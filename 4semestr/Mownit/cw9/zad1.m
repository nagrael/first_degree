X = (rgb2gray(imread('galia.png')));
Y = (rgb2gray(imread('galia_e.png')));
 X = imcomplement(X);
 Y = imcomplement(Y);



F  = fft2(X);

figure, imshow(log(abs(fftshift(F))+1),[]), colormap gray
title('Image FFT2 Magnitude')
figure, imshow(angle(fftshift(F))), colormap gray
title('Image FFT2 Phase')
[h,w] = size(X);


C=real(ifft2(fft2(X).*fft2(rot90(Y,2),h,w)));
max(C(:))
thresh = 0.9*max(C(:)) ; % Use a threshold that's a little less than max.
D = C > thresh;
sum(D(:)==1)
se = strel('disk',7);
E = imdilate(D,se);
Z = 255 *E;
figure
imshow(imcomplement(X)-uint8(Z)) % Display pixels with values over the threshold.