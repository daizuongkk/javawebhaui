package com.daizuongkk.web.dto.request;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
@Builder
public class SearchProductRequest {
    private String name;
    private List<String> categories;
    private List<String> brands;
    private Double minPrice;
    private Double maxPrice;
    private String sortBy;
}
