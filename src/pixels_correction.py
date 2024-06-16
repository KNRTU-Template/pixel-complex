import cv2
import numpy as np

def restore_broken_pixels(image):
    UNDER_ILLUMINATED_THRESHOLD = 0.15
    OVER_ILLUMINATED_THRESHOLD = 5.0
    
    kernel_size = 3
    
    blurred_image = np.zeros_like(image)
    for channel in range(image.shape[2]):
        blurred_image[:, :, channel] = cv2.medianBlur(image[:, :, channel], kernel_size)

    correction_report = []
    
    for channel in range(image.shape[2]):
        b_threshold = UNDER_ILLUMINATED_THRESHOLD * np.mean(image[:,:,channel])
        u_threshold = OVER_ILLUMINATED_THRESHOLD * np.mean(image[:,:,channel])
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                pixel_value = image[i, j, channel]
                if pixel_value == 0 or pixel_value < b_threshold or pixel_value > u_threshold:
                    corrected_value = blurred_image[i, j, channel]
                    correction_report.append(f"{i}; {j}; {channel + 1}; {pixel_value}; {corrected_value}")
                    image[i, j, channel] = corrected_value

    return image, correction_report