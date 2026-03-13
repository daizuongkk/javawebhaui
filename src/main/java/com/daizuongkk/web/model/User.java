package com.daizuongkk.web.model;

import lombok.*;

import java.util.Date;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class User {
	private Long id;
	private String username;
	private String password;
	private String firstName;
	private String lastName;
	private Role role;
	private String avtUrl;
	private  String phone;
	private String email;
	private Boolean active;
	private Date createdAt;
	private Date updatedAt;
}
