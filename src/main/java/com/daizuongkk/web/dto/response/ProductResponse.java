package com.daizuongkk.web.dto.response;


import lombok.*;

import java.util.Date;
import java.util.List;

@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ProductResponse {
    private Long id;
    private String name;
    private String description;
    private  String detail;
    private  String summary;
    private String category;
    private Double price;
    private List<String> imageUrl;
    private Long promotion;

    private Long reviewScore;
    private Date createdAt;

}
