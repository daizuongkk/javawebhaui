package com.daizuongkk.web.model;

import java.util.HashMap;
import java.util.Map;

public enum Brand {

    SAMSUNG("Sam Sung"), APPLE("Apple"), OPPO("Oppo"), XIAOMI("Xiaomi");

    private final String name;

    Brand(String name) {
        this.name = name;
    }

    public static Map<String, String> getAlls() {
        Map<String, String> brands = new HashMap<String, String>();
        for (Brand brand : Brand.values()) {
            brands.put(brand.toString(), brand.name);
        }
        return brands;
    }

}
