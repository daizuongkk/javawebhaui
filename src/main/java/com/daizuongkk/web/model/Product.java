package com.daizuongkk.web.model;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Builder
public class Product {
	private Long id;
	private String name;
	private String code;
	private String type;
	private String imgUrl;
	private String description;
	private Double price;

}
