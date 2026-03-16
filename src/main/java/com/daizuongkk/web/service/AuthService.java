package com.daizuongkk.web.service;

import com.daizuongkk.web.dto.response.UserResponse;
import com.daizuongkk.web.model.Role;
import com.daizuongkk.web.model.User;
import com.daizuongkk.web.repository.UserRepository;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;
import org.mindrot.jbcrypt.BCrypt;

import java.util.regex.Pattern;

public class AuthService {
    private final UserRepository userRepository;
    private static final Pattern USERNAME_PATTERN = Pattern.compile("^[A-Za-z][A-Za-z0-9._]{6,31}$");
    private static final Pattern EMAIL_PATTERN = Pattern.compile("^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$");
    private static final Pattern PASSWORD_PATTERN =
            Pattern.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[^A-Za-z0-9]).{8,32}$");
    public enum RegisterStatus {
        SUCCESS,
        INVALID_INPUT,
        INVALID_USERNAME_FORMAT,
        INVALID_EMAIL_FORMAT,
        INVALID_PASSWORD_FORMAT,
        USERNAME_EXISTS,
        EMAIL_EXISTS,
        FAILED
    }

    public AuthService() {
        this.userRepository = new UserRepository();
    }

    public AuthService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public UserResponse login(String username, String password) {
        if (username == null || password == null) {
            return null;
        }

        String normalizedUsername = username.trim();
        if (normalizedUsername.isEmpty() || password.isEmpty()) {
            return null;
        }

        User user = userRepository.findByUsernameOrEmail(normalizedUsername);
        if (user == null) {
            return null;
        }
        if (!matchesPassword(password, user.getPassword())) {
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

    public RegisterStatus register(String username, String email, String password) {
        if (username == null || email == null || password == null) {
            return RegisterStatus.INVALID_INPUT;
        }

        String normalizedUsername = username.trim();
        String normalizedEmail = email.trim().toLowerCase();

        if (normalizedUsername.isEmpty() || normalizedEmail.isEmpty() || password.isEmpty()) {
            return RegisterStatus.INVALID_INPUT;
        }

        if (!isValidUsernameFormat(normalizedUsername)) {
            return RegisterStatus.INVALID_USERNAME_FORMAT;
        }

        if (!isValidEmailFormat(normalizedEmail)) {
            return RegisterStatus.INVALID_EMAIL_FORMAT;
        }

        if (!isValidPasswordFormat(password)) {
            return RegisterStatus.INVALID_PASSWORD_FORMAT;
        }

        if (userRepository.existsByUsername(normalizedUsername)) {
            return RegisterStatus.USERNAME_EXISTS;
        }

        if (userRepository.existsByEmail(normalizedEmail)) {
            return RegisterStatus.EMAIL_EXISTS;
        }

        User user = User.builder()
                .username(normalizedUsername)
                .email(normalizedEmail)
                .password(hashPassword(password))
                .role(Role.CUSTOMER)
                .build();

        return userRepository.create(user) ? RegisterStatus.SUCCESS : RegisterStatus.FAILED;
    }

    public static boolean isValidUsernameFormat(String username) {
        return username != null && USERNAME_PATTERN.matcher(username).matches();
    }

    public static boolean isValidEmailFormat(String email) {
        return email != null && EMAIL_PATTERN.matcher(email).matches();
    }

    public static boolean isValidPasswordFormat(String password) {
        return password != null && PASSWORD_PATTERN.matcher(password).matches();
    }

    private boolean matchesPassword(String rawPassword, String storedPassword) {
        if (storedPassword == null) {
            return false;
        }

        if (storedPassword.startsWith("$2a$") || storedPassword.startsWith("$2b$") || storedPassword.startsWith("$2y$")) {

            return BCrypt.checkpw(rawPassword, storedPassword);
        }

        // Backward compatible for old plaintext records.
        return storedPassword.equals(rawPassword);
    }

    private String hashPassword(String rawPassword) {
        return BCrypt.hashpw(rawPassword, BCrypt.gensalt(12));
    }

}
