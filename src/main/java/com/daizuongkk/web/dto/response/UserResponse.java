package com.daizuongkk.web.dto.response;

import com.daizuongkk.web.model.Role;
import lombok.*;

@Builder
@NoArgsConstructor
@AllArgsConstructor
@Setter
@Getter
public class UserResponse {
    private String username;
    private String firstName;
    private String lastName;
    private Role role;
    private String avtUrl;
    private  String phone;
    private String email;
    private Boolean verified;
    private String status;

}
