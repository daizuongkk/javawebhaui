package com.daizuongkk.web.model;

import lombok.Getter;

import java.util.HashMap;
import java.util.Map;
@Getter
public   enum Category {

    DIEN_THOAI("Điện Thoại"), LAPTOP("Máy Tính"), CAMERA("Máy Ảnh"), PHU_KIEN("Phụ Kiện");

    private final String name;

    Category(String name) {
        this.name = name;
    }

    public static Map<String, String> getAlls() {
       Map<String, String> categories = new HashMap<String, String>();
        for (Category category : Category.values()) {
            categories.put(category.toString(), category.name);
        }
        return categories;
    }



    public static String getNameByCode(String category) {
        for (Category ctgr : Category.values()) {
        if (ctgr.toString().equals(category)) {}
                return ctgr.getName();
            }
        return category;
    }


}
