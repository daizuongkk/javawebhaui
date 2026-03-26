package com.daizuongkk.web.service;

import com.daizuongkk.web.model.ProductImg;
import com.daizuongkk.web.repository.ProductImgRepository;

import java.util.Collections;
import java.util.List;
import java.util.regex.Pattern;

public class ProductImgService {
    private static final Pattern IMAGE_URL_PATTERN =
            Pattern.compile("^(https?://.+|/.+)$", Pattern.CASE_INSENSITIVE);

    private final ProductImgRepository productImgRepository;

    public ProductImgService() {
        this.productImgRepository = new ProductImgRepository();
    }

    public ProductImgService(ProductImgRepository productImgRepository) {
        this.productImgRepository = productImgRepository;
    }

    public List<ProductImg> getImagesByProductId(Long productId) {
        if (!isValidProductId(productId)) {
            return Collections.emptyList();
        }
        return productImgRepository.findByProductId(productId);
    }

    public List<String> getImageUrlsByProductId(Long productId) {
        if (!isValidProductId(productId)) {
            return Collections.emptyList();
        }
        return productImgRepository.findUrlsByProductId(productId);
    }

    public String getPrimaryImageUrl(Long productId) {
        if (!isValidProductId(productId)) {
            return null;
        }
        return productImgRepository.findPrimaryUrlByProductId(productId);
    }

    public boolean addImage(Long productId, String imageUrl) {
        if (!isValidProductId(productId) || !isValidImageUrl(imageUrl)) {
            return false;
        }
        return productImgRepository.create(productId, imageUrl);
    }

    public int addImages(Long productId, List<String> imageUrls) {
        if (!isValidProductId(productId) || imageUrls == null || imageUrls.isEmpty()) {
            return 0;
        }
        return productImgRepository.createBatch(productId, imageUrls);
    }

    public int replaceAllImages(Long productId, List<String> imageUrls) {
        if (!isValidProductId(productId)) {
            return 0;
        }
        return productImgRepository.replaceAllByProductId(productId, imageUrls);
    }

    public boolean removeAllImages(Long productId) {
        if (!isValidProductId(productId)) {
            return false;
        }
        return productImgRepository.deleteByProductId(productId);
    }

    private boolean isValidProductId(Long productId) {
        return productId != null && productId > 0;
    }

    private boolean isValidImageUrl(String imageUrl) {
        if (imageUrl == null) {
            return false;
        }

        String normalized = imageUrl.trim();
        if (normalized.isEmpty() || normalized.length() > 2048) {
            return false;
        }

        return IMAGE_URL_PATTERN.matcher(normalized).matches();
    }
}

