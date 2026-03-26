package com.daizuongkk.web.model;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

import java.util.Date;

@Getter
@Setter
@Builder
public class Product {
	private Long id;
	private String name;
	private String description;
	private String detail;
	private String summary;
	private Double price;
	private String brand;
	private Date createdAt;
	private Date updatedAt;
	private String category;
	private Long promotion;

}
