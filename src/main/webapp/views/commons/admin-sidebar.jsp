<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<%--
  Created by IntelliJ IDEA.
  User: daizuongkk
  Date: 3/21/2026
  Time: 3:37 PM
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<base href="${pageContext.request.contextPath}/">

<aside id="sidebar" class="sidebar">
    <div class="logo-area">
        <a href="admin/dashboard" class="d-inline-flex"><img
                src="data:image/svg+xml,%3csvg%20width='62'%20height='67'%20viewBox='0%200%2062%2067'%20fill='none'%20xmlns='http://www.w3.org/2000/svg'%3e%3cpath%20d='M30.604%2066.378L0.00805664%2048.1582V35.7825L30.604%2054.0023V66.378Z'%20fill='%23302C4D'/%3e%3cpath%20d='M61.1996%2048.1582L30.604%2066.378V54.0023L61.1996%2035.7825V48.1582Z'%20fill='%23E66239'/%3e%3cpath%20d='M30.5955%200L0%2018.2198V30.5955L30.5955%2012.3757V0Z'%20fill='%23657E92'/%3e%3cpath%20d='M61.191%2018.2198L30.5955%200V12.3757L61.191%2030.5955V18.2198Z'%20fill='%23A3B2BE'/%3e%3cpath%20d='M30.604%2048.8457L0.00805664%2030.6259V18.2498L30.604%2036.47V48.8457Z'%20fill='%23302C4D'/%3e%3cpath%20d='M61.1996%2030.6259L30.604%2048.8457V36.47L61.1996%2018.2498V30.6259Z'%20fill='%23E66239'/%3e%3c/svg%3e"
                alt="" width="24">
            <span class="logo-text ms-2"> <img src="./assets/img/logo.svg" alt=""></span>
        </a>
    </div>
    <ul class="nav flex-column">
        <li class="px-4 py-2"><small class="nav-text">Main</small></li>
        <li><a class="nav-link active" href="admin?page=dashboard"><i class="ti ti-home"></i><span
                class="nav-text">Thống Kê</span></a></li>
        <li><a class="nav-link" href="<c:url value='admin?page=inventory'/>"><i class="ti ti-box-seam"></i><span
                class="nav-text">Kho</span></a></li>
        <li><a class="nav-link" href="<c:url value='admin?page=add-product'/>"><i class="ti ti-plus"></i><span class="nav-text">Thêm Sản Phẩm</span></a>
        </li>
        <li><a class="nav-link" href="<c:url value='admin?page=reports'/>"><i class="ti ti-receipt"></i><span class="nav-text">Báo Cáo</span></a>
        </li>

      <li class="px-4 py-2"><small class="nav-text">Account</small></li>

        <li>
            <a class="nav-link" href="admin/users">
                <i class="ti ti-logout"></i>
                <span class="nav-text">Người Dùng</span>
            </a>
        </li>

        <li>
            <a class="nav-link" href="logout">
                <i class="ti ti-logout"></i>
                <span class="nav-text">Đăng Xuất</span>
            </a>
        </li>
    </ul>

</aside>
