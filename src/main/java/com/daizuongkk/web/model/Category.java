package com.daizuongkk.web.model;

import java.util.ArrayList;
import java.util.List;

public enum Category {

    DIEN_THOAI("Điện Thoại"), LAPTOP("Máy Tính"), CAMERA("Máy Ảnh"), PHU_KIEN("Phụ Kiện");

    private String name;

    Category(String s) {
        this.name = name;
    }

    public List<String> getAllCategory() {
        List<String> categories = new ArrayList<>();
        for (Category category : Category.values()) {
            categories.add(category.name);
        }
        return categories;
    }
}
