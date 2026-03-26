package com.daizuongkk.web.util;

public class PaginationUtils {

    public static int parsePositiveInt(String rawValue, int defaultValue) {
        if (rawValue == null || rawValue.trim().isEmpty()) {
            return defaultValue;
        }

        try {
            int parsed = Integer.parseInt(rawValue.trim());
            return parsed > 0 ? parsed : defaultValue;
        } catch (NumberFormatException ex) {
            return defaultValue;
        }
    }

}
