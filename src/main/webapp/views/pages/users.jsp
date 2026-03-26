<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<base href="${pageContext.request.contextPath}/">

<!DOCTYPE html>
<html lang="en">

<head>
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
<%@include file="../commons/admin-sidebar.jsp" %>

<!-- MAIN CONTENT -->
<main id="content" class="content py-10">
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <div class="">
                        <h1 class="fs-3 mb-1">Quản Lí Tài Khoản</h1>
                        <p class="mb-0">Trang quản lí danh sách tài khoản</p>
                    </div>
                    <div>
                        <a href="create-product.jsp" class="btn btn-primary">Thêm Người Dùng</a>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-12">
                <div>
                    <div class="d-flex gap-2 mb-3 flex-wrap justify-content-between">
                        <input type="text" class="form-control" placeholder="Search products..."
                               style="max-width: 250px;">
                        <div class="d-flex gap-2">

                            <button class="btn btn-outline-secondary">
                                <i class="ti ti-filter"></i> Filter
                            </button>
                            <button class="btn btn-outline-secondary">
                                <i class="ti ti-file-excel"></i> Excel
                            </button>
                            <button class="btn btn-outline-secondary">
                                <i class="ti ti-file-pdf"></i> PDF
                            </button>
                        </div>
                    </div>
                </div>
                <div class="card table-responsive ">
                    <table class="table mb-0 text-nowrap table-hover">
                        <thead class="table-light border-light">
                        <tr>
                            <th>Image</th>

                            <th>Code</th>
                            <th>Category</th>
                            <th>Brand</th>
                            <th>Price</th>
                            <th>Unit</th>
                            <th>Quantity</th>
                            <th>Action</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr class="align-middle ">
                            <td><a href=""><img src="./assets/img/product-1.png" alt=""
                                                class="avatar avatar-md rounded"/><span
                                    class="ms-3">Gaming Joy Stick</span></a>
                            </td>

                            <td>PRD001</td>
                            <td>Electronics</td>
                            <td>Brand Name</td>
                            <td>$99.99</td>
                            <td>pcs</td>
                            <td>150</td>
                            <td class="">
                                <a href="#" class=""><i class="ti ti-edit "></i></a>
                                <a href="#" class="link-danger"><i class="ti ti-trash ms-2"></i></a>
                            </td>
                        </tr>
                        <tr class="align-middle">
                            <td><a href=""><img src="./assets/img/product-2.png" alt=""
                                                class="avatar avatar-md rounded"/><span
                                    class="ms-3">Wireless Earphones</span></a>
                            </td>
                            <td>PRD002</td>
                            <td>Electronics</td>
                            <td>Tech Pro</td>
                            <td>$89.99</td>
                            <td>pcs</td>
                            <td>320</td>
                            <td class="">
                                <a href="#" class=""><i class="ti ti-edit "></i></a>
                                <a href="#" class="link-danger"><i class="ti ti-trash ms-2"></i></a>
                            </td>
                        </tr>
                        <tr class="align-middle">
                            <td><a href=""><img src="./assets/img/product-3.png" alt=""
                                                class="avatar avatar-md rounded"/><span
                                    class="ms-3">Smart Watch Pro</span></a>
                            </td>
                            <td>PRD003</td>
                            <td>Electronics</td>
                            <td>Tech Pro</td>
                            <td>$98.00</td>
                            <td>pcs</td>
                            <td>200</td>
                            <td class="">
                                <a href="#" class=""><i class="ti ti-edit "></i></a>
                                <a href="#" class="link-danger"><i class="ti ti-trash ms-2"></i></a>
                            </td>
                        </tr>
                        <tr class="align-middle">
                            <td><a href=""><img src="./assets/img/product-4.png" alt=""
                                                class="avatar avatar-md rounded"/><span
                                    class="ms-3">USB-C Fast Charger</span></a>
                            </td>
                            <td>PRD004</td>
                            <td>Electronics</td>
                            <td>Tech Pro</td>
                            <td>$86.00</td>
                            <td>pcs</td>
                            <td>80</td>
                            <td class="">
                                <a href="#" class=""><i class="ti ti-edit "></i></a>
                                <a href="#" class="link-danger"><i class="ti ti-trash ms-2"></i></a>
                            </td>
                        </tr>
                        <tr class="align-middle">
                            <td><a href=""><img src="./assets/img/product-5.png" alt=""
                                                class="avatar avatar-md rounded"/><span class="ms-3">Portable Bluetooth Speaker</span></a>
                            </td>
                            <td>PRD005</td>
                            <td>Electronics</td>
                            <td>Tech Pro</td>
                            <td>$32.00</td>
                            <td>pcs</td>
                            <td>110</td>
                            <td class="">
                                <a href="#" class=""><i class="ti ti-edit "></i></a>
                                <a href="#" class="link-danger"><i class="ti ti-trash ms-2"></i></a>
                            </td>
                        </tr>
                        <tr class="align-middle">
                            <td><a href=""><img src="./assets/img/product-6.png" alt=""
                                                class="avatar avatar-md rounded"/><span
                                    class="ms-3">Magic Keyboard</span></a>
                            </td>
                            <td>PRD006</td>
                            <td>Electronics</td>
                            <td>Tech Pro</td>
                            <td>$49.00</td>
                            <td>pcs</td>
                            <td>10</td>
                            <td class="">
                                <a href="#" class=""><i class="ti ti-edit "></i></a>
                                <a href="#" class="link-danger"><i class="ti ti-trash ms-2"></i></a>
                            </td>
                        </tr>
                        <tr class="align-middle">
                            <td><a href=""><img src="./assets/img/product-7.png" alt=""
                                                class="avatar avatar-md rounded"/><span
                                    class="ms-3">MacBook Pro 16"</span></a>
                            </td>
                            <td>PRD007</td>
                            <td>Electronics</td>
                            <td>Tech Pro</td>
                            <td>$99.00</td>
                            <td>pcs</td>
                            <td>10</td>
                            <td class="">
                                <a href="#" class=""><i class="ti ti-edit "></i></a>
                                <a href="#" class="link-danger"><i class="ti ti-trash ms-2"></i></a>
                            </td>
                        </tr>
                        <tr class="align-middle">
                            <td><a href=""><img src="./assets/img/product-8.png" alt=""
                                                class="avatar avatar-md rounded"/><span
                                    class="ms-3">Wireless Earphones</span></a>
                            </td>
                            <td>PRD008</td>
                            <td>Electronics</td>
                            <td>Tech Pro</td>
                            <td>$109.00</td>
                            <td>pcs</td>
                            <td>200</td>
                            <td class="">
                                <a href="#" class=""><i class="ti ti-edit "></i></a>
                                <a href="#" class="link-danger"><i class="ti ti-trash ms-2"></i></a>
                            </td>
                        </tr>
                        </tbody>
                        <tfoot class="">

                        <tr>
                            <td class="border-bottom-0">Showing product per page</td>
                            <td colspan="9" class="border-bottom-0">
                                <nav aria-label="Page navigation" class="d-flex justify-content-end">
                                    <ul class="pagination mb-0">
                                        <li class="page-item disabled">
                                            <a class="page-link" href="#" tabindex="-1">Previous</a>
                                        </li>
                                        <li class="page-item active"><a class="page-link" href="#">1</a></li>
                                        <li class="page-item"><a class="page-link" href="#">2</a></li>
                                        <li class="page-item"><a class="page-link" href="#">3</a></li>
                                        <li class="page-item">
                                            <a class="page-link" href="#">Next</a>
                                        </li>
                                    </ul>
                                </nav>
                            </td>
                        </tr>

                        </tfoot>
                    </table>
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


</body>

</html>