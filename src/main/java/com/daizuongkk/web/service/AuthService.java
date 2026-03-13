package com.daizuongkk.web.service;

import com.daizuongkk.web.dto.response.UserResponse;
import com.daizuongkk.web.model.User;
import com.daizuongkk.web.repository.UserRepository;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
public class AuthService {
    private UserRepository userRepository;

    public UserResponse login(String username, String password) {
        User user = userRepository.findByUsernameOrEmail(username);
        if (user == null) {
            return null;
        }
        if (!user.getPassword().equals(password)) {
            return null;
        }

        return UserResponse.builder()
                .username(user.getUsername())
                .firstName(user.getFirstName())
                .lastName(user.getLastName())
                .role(user.getRole())
                .avtUrl(user.getAvtUrl())
                .phone(user.getPhone())
                .email(user.getEmail())
                .active(user.getActive())
                .build();
    }

}
