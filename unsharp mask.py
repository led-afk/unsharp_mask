import cv2 #xulyanh
import numpy as np #xulymatran
import streamlit as st #giaodien

uploaded_image = st.file_uploader("Upload ảnh",type = ["jpg","png","jpeg"]) #nut de nguoi dung up anh tu may tinh

if uploaded_image is not None:
    #doc du lieu tho duoc up len -> phan loai thanh byte -> chuyen byte thanh mang
    file_bytes = np.asanyarray(bytearray(uploaded_image.read()), dtype = np.uint8)
    # dua mang ve dang ma tran mau
    image = cv2.imdecode(file_bytes, 1)

    if image is None:
        st.error("Không có ảnh")
    else:

        h, w, c = image.shape
        anh_goc = image
        col1, col2 = st.columns(2) #chia giao dien thanh 2 cot
        
        with col1:
            st.subheader("Ảnh gốc")
            # dung cvtcolor de chuyen tu bgr sang rgb vi opencv doc anh theo bgr va st doc anh theo rgb
            st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), use_container_width=True)

        with st.spinner("Hold on bro"):

            pad = 1
            padded = np.pad(image, ((pad, pad), (pad, pad), (0,0)), mode='constant')

            gaussian = np.array([[0.0625, 0.125, 0.0625],
                               [0.125, 0.25, 0.125],
                               [0.0625, 0.125, 0.0625]])
            #tao anh rong toan mau den kich co = anh goc
            after_blur = np.zeros_like(image)

            for x in range(h):
                for y in range(w):
                    for z in range(c):
                        a = 0.0
                        for b in range(3):
                            for d in range(3):
                                pixel = padded[x+b, y+d, z]
                                weight = gaussian[b, d]
                                a += pixel * weight
                        
                        after_blur[x, y, z] = np.clip(a, 0 , 255)
            output = 2*anh_goc.astype(np.float32) - after_blur.astype(np.float32)
            output = np.clip(output, 0, 255).astype(np.uint8)

            with col2:
                st.subheader("done roi ni'")
                # chuyen output tu bgr sang rgb
                output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
                st.image(output_rgb, use_container_width=True)

                
            


        