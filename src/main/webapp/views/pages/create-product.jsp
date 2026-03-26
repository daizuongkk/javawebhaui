<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<base href="${pageContext.request.contextPath}/">

<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8"/>
    <title>Admin - Thêm Sản Phẩm</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="apple-touch-icon" sizes="180x180" href="./assets/img/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="./assets/img/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="./assets/img/favicon-16x16.png">
    <link rel="manifest" href="./assets/site.webmanifest">
    <link rel="stylesheet" href="assets/css/font-awesome.min.css">
    <script type="module" crossorigin src="./assets/js/admin.js"></script>
    <link rel="stylesheet" crossorigin href="./assets/css/admin.css">
</head>

<body>
<div id="overlay" class="overlay"></div>
<!-- TOPBAR -->
<%@include file="../commons/admin-header.jsp"%>

<!-- SIDEBAR -->

<%@include file="../commons/admin-sidebar.jsp"%>


<!-- MAIN CONTENT -->
<main id="content" class="content py-10">
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-4 gap-3">
                    <div class="">
                        <h1 class="fs-3 mb-1">Add Inventory</h1>
                        <p class="mb-0">Manage your inventory items</p>
                    </div>
                    <div>
                        <a href="admin?page=inventory" class="btn btn-primary">Danh Sách Sản Phẩm</a>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-body p-4">
                        <form id="addProductForm">
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label for="productName" class="form-label">Product Name</label>
                                    <input type="text" class="form-control" id="productName"
                                           placeholder="Enter product name" required>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label for="productSKU" class="form-label">SKU</label>
                                    <input type="text" class="form-control" id="productSKU" placeholder="Enter SKU"
                                           required>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label for="productPrice" class="form-label">Price</label>
                                    <input type="number" class="form-control" id="productPrice" placeholder="0.00"
                                           step="0.01" required>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label for="productStock" class="form-label">Stock Quantity</label>
                                    <input type="number" class="form-control" id="productStock" placeholder="0"
                                           required>
                                </div>
                            </div>

                            <div class="mb-3">
                                <label for="productCategory" class="form-label">Category</label>
                                <select class="form-select" id="productCategory" required>
                                    <option value="">Select category</option>
                                    <option value="electronics">Electronics</option>
                                    <option value="clothing">Clothing</option>
                                    <option value="food">Food</option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label for="productImage" class="form-label">Product Image</label>
                                <input type="file" class="form-control" id="productImage" accept="image/*" required>
                            </div>
                            <div class="mb-3">
                                <label for="productDescription" class="form-label">Description</label>
                                <textarea class="form-control" id="productDescription" rows="4"
                                          placeholder="Enter product description"></textarea>
                            </div>
                            <div class="d-flex gap-2">
                                <button type="submit" class="btn btn-primary">Add Product</button>
                                <button type="reset" class="btn btn-secondary">Clear</button>
                            </div>

                        </form>
                    </div>
                </div>


            </div>

        </div>

        <div class="row">
            <div class="col-12">
                <footer class="text-center py-2 mt-6 text-secondary ">
                    <p class="mb-0">Copyright © 2026 InApp Inventory Dashboard. Developed by <a
                            href="https://codescandy.com/" target="_blank" class="text-primary">CodesCandy</a> •
                        Distributed by <a href="https://themewagon.com/" target="_blank"
                                          class="text-primary">ThemeWagon</a></p>
                </footer>
            </div>

        </div>

    </div>
</main>

<!-- Bootstrap JS -->

<%@ include file="../commons/script.jsp" %>

</body>

</html>