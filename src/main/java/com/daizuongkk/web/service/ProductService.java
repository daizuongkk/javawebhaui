package com.daizuongkk.web.service;

import com.daizuongkk.web.dto.request.SearchProductRequest;
import com.daizuongkk.web.dto.response.ProductResponse;
import com.daizuongkk.web.model.Category;
import com.daizuongkk.web.model.Product;
import com.daizuongkk.web.repository.ProductImgRepository;
import com.daizuongkk.web.repository.ProductRepository;
import com.daizuongkk.web.repository.ReviewRepository;
import org.modelmapper.ModelMapper;

import java.util.ArrayList;
import java.util.List;

public class ProductService {

    private final ModelMapper modelMapper = new ModelMapper();

    private final ProductRepository productRepository;
    private final ProductImgRepository productImgRepository;
    private final ReviewRepository reviewRepository;

    public ProductService() {
        this.productRepository = new ProductRepository();
        this.productImgRepository = new ProductImgRepository();
        this.reviewRepository = new ReviewRepository();
    }

    public ProductService(ProductRepository productRepository,
                          ProductImgRepository productImgRepository,
                          ReviewRepository reviewRepository) {
        this.productRepository = productRepository != null ? productRepository : new ProductRepository();
        this.productImgRepository = productImgRepository != null ? productImgRepository : new ProductImgRepository();
        this.reviewRepository = reviewRepository != null ? reviewRepository : new ReviewRepository();
    }


    public List<ProductResponse> getAllProducts() {

        List<Product> products = productRepository.findAll();
        List<ProductResponse> productResponseList = new ArrayList<>();

        for (Product product : products) {
            productResponseList.add(productToProductResponse(product));
        }
        return productResponseList;
    }

    public List<ProductResponse> getProductsByPage(int page, int size) {
        List<Product> products =  productRepository.findPage(page, size);
        List<ProductResponse> productResponseList = new ArrayList<>();

        for (Product product : products) {
            productResponseList.add(productToProductResponse(product));
        }
        return productResponseList;
    }

    public ProductResponse getProductById(Long id) {

        return productToProductResponse(productRepository.findById(id))  ;
    }

    public List<Product> getProductsByCategory(String category) {
        return productRepository.findByCategory(category);
    }

    public List<Product> searchProductsByName(String keyword) {
        return productRepository.searchByName(keyword);
    }

    public List<ProductResponse> getLatestProducts(int limit) {

        List<ProductResponse> productResponses = new ArrayList<>();

        List<Product> products =  productRepository.findLatest(limit);

        for (Product product : products) {
            productResponses.add(productToProductResponse(product));
        }
        return productResponses;
    }

    public Long countProducts() {
        return productRepository.countAll();
    }


    private ProductResponse productToProductResponse(Product product) {
        ProductResponse productResponse = this.modelMapper.map(product, ProductResponse.class);
        List<String> imageUrls = productImgRepository.findUrlsByProductId(product.getId());
      productResponse.setCategory(Category.getNameByCode(product.getCategory()));

        productResponse.setImageUrl(imageUrls);

        Long reviewScore = reviewRepository.findAverageScoreByProductId(product.getId()).longValue();
        productResponse.setReviewScore(reviewScore);


        return productResponse;

    }

    public Long countProductsByFilter(SearchProductRequest filters) {

        return productRepository.countByFilter(filters);
    }

    public List<ProductResponse> getProductsByFilter(int currentPage, int size, SearchProductRequest filters) {
        List<Product> products = productRepository.findByFilter(currentPage, size, filters);
        List<ProductResponse> productResponseList = new ArrayList<>();

        for (Product product : products) {
            productResponseList.add(productToProductResponse(product));
        }
        return productResponseList;

    }
}
