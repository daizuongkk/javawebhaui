package com.daizuongkk.web.model;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@Builder
public class ProductImg {
    private Long id;
    private Long productId;
    private String url;

}
