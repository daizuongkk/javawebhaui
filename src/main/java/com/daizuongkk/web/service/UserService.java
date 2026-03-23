package com.daizuongkk.web.service;

import com.daizuongkk.web.model.User;
import com.daizuongkk.web.repository.UserRepository;

public class UserService {
    private UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }


    public User findById(Long id) {
        return userRepository.findById(id);
    }

}
