<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Exam Portal</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

    <style>

        body{
            background-color:#f8f9fa;
        }

        /* Navbar */

        .navbar{
            background: linear-gradient(135deg, #2563eb, #1e40af);
            padding: 8px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
        }

        .navbar-brand{
            font-size: 32px;
            font-weight: 700;
        }

        .nav-link{
            color:white !important;
            font-weight:500;
            margin-left:10px;
            transition: all 0.3s ease;
        }

        .nav-link:hover{
            color:#ffd700 !important;
            transform: translateY(-2px);
        }

        /* Search */

        .search-input{
            width:170px;
            height:38px;
        }

        .search-btn{
            transition: all 0.3s ease;
        }

        .search-btn:hover{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(255,255,255,0.3);
        }

        /* Content */

        .main-content{
            min-height:75vh;
        }

        /* Footer */

        footer{
            margin-top:50px;
        }

    </style>
</head>

<body>

<nav class="navbar navbar-expand-lg navbar-dark">

    <div class="container">

        <a class="navbar-brand" href="{{ url_for('home') }}">
            🎓 Smart Exam Portal
        </a>

        <button class="navbar-toggler"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#navbarContent">

            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse justify-content-end"
             id="navbarContent">

            <ul class="navbar-nav align-items-center">

                <li class="nav-item">
                    <a class="nav-link"
                       href="{{ url_for('home') }}">
                        🏠 Home
                    </a>
                </li>

                <li class="nav-item">
                    <a class="nav-link"
                       href="{{ url_for('records') }}">
                        📚 Records
                    </a>
                </li>
            {% if session.get('role') == 'admin' %}
                <li class="nav-item">
                    <a class="nav-link"
                       href="{{ url_for('add_students') }}">
                        👨‍🎓 Add Student
                    </a>
                </li>
            {% endif %}

                <li class="nav-item">
                    <a class="nav-link"
                       href="{{ url_for('exam') }}">
                        📝 Start Exam
                    </a>
                </li>
                 {% if session.get('username') %}

<li class="nav-item me-2">
    <span class="badge bg-warning text-dark fs-6 p-2">
        👤 {{ session['username'] }}
    </span>
</li>

<li class="nav-item">
    <a class="nav-link"
       href="{{ url_for('logout') }}">
        🚪 Logout
    </a>
</li>

{% else %}

<li class="nav-item">
    <a class="nav-link"
       href="{{ url_for('login') }}">
        🔐 Login
    </a>
</li>

<li class="nav-item">
    <a class="nav-link"
       href="{{ url_for('register') }}">
        🆕 Register
    </a>
</li>

{% endif %}
                
            </ul>

            <form class="d-flex ms-lg-3 mt-2 mt-lg-0 position-relative"
                  action="{{ url_for('search') }}"
                  method="GET">

                <input
                    id="searchInput"
                    class="form-control me-2 rounded-pill search-input"
                    type="search"
                    placeholder="🔍 Search Student"
                    name="q"
                    autocomplete="off">

                <button
                    class="btn btn-warning fw-bold rounded-pill px-3 search-btn"
                    type="submit">

                    Search

                </button>

                <div id="suggestions"
                     class="list-group position-absolute"
                     style="top:45px; width:250px; z-index:1000;">
                </div>

            </form>

        </div>

    </div>

</nav>

<div class="container mt-4 main-content">

    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}

            {% for category, message in messages %}

                <div class="alert alert-{{ category }}">
                    {{ message }}
                </div>

            {% endfor %}

        {% endif %}
    {% endwith %}

    {% block content %}
    {% endblock %}

</div>

<footer class="bg-dark text-white text-center p-3">
    © 2026 Smart Exam Portal
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
background-color:#f8f9fa;
 background-color:#f8f9fa;

 '''home.html

{% extends "base.html" %}

{% block content %}

<h2 class="text-center mb-4">
    Welcome to Smart Exam Portal
</h2>
<div class="row g-4">
    <div class="col-md-4">
        <div class="card shadow">
            <div class="card-body text-center">
                <h5>Total Students</h5>
                <span class="badge bg-primary">
                    {{ students|length }}
                </span>
            </div>
        </div>
    </div>

    <div class="col-md-4">
        <div class="card shadow">
            <div class="card-body text-center">
                <h5>✅Passed Students</h5>
                <span class="badge bg-success">
                    {{ passed_students }}
                </span>
            </div>
        </div>
    </div>

    <div class="col-md-4">
        <div class="card shadow">
            <div class="card-body text-center">
                <h5>❌Failed Students</h5>
                <span class="badge bg-danger">
                    {{ failed_students }}
                </span>
            </div>
        </div>
    </div>

</div>
<div class="row mt-3">
    <div class="col-md-4">
        <div class="card shadow">
           <div class="card-body text-center">
              <h5>Total Attempts</h5>
              <span class="badge bg-info">
                {{ total_attempts }}
               </span>
            </div>
        </div>
    </div>

    <div class="col-md-4">
        <div class="card shadow">
            <div class="card-body text-center">
               <h5>Average Score</h5>
               <span class="badge bg-warning text-dark">
                {{ average_score|round(2) }}
               </span>
            </div>
        </div>
    </div>


      <div class="col-md-4">
           <div class="card shadow">
                <div class="card-body text-center">
                     <h5>Highest Score</h5>
                     <span class="badge bg-dark">
                      {{ highest_score }}
                     </span>
        
                </div>
            </div>
        </div>
</div>
<div class="card mt-4 shadow">
    <div class="card-body">
        <h4>Project Features</h4>

        <ul>
            <li>Online MCQ Tests</li>
            <li>Student Records</li>
            <li>Score Calculation</li>
            <li>Percentage Calculation</li>
            <li>Pass / Fail Result</li>
        </ul>
    </div>
</div>

{% endblock %}'''

'''record.html
{% extends "base.html" %}

{% block content %}

<h2 class="mb-3">Student Records</h2>

<form method="GET" action="{{ url_for('records') }}" class="mb-3">

    <select name="status" class="form-select w-25 d-inline">

        <option value=""
            {% if request.args.get('status') == '' %}selected{% endif %}>
            All Students
        </option>

        <option value="pass"
            {% if request.args.get('status') == 'pass' %}selected{% endif %}>
            Pass Students
        </option>

        <option value="fail"
            {% if request.args.get('status') == 'fail' %}selected{% endif %}>
            Fail Students
        </option>

    </select>

    <button type="submit" class="btn btn-primary">
        Filter
    </button>

</form>

<div class="container">

    <div class="row">

        <!-- Student Table -->
        <div class="col-md-8">

            <table class="table table-striped table-hover table-bordered">

                <thead class="table-dark">
                    <tr>
                        <th>No</th>
                        <th>Roll No</th>
                        <th>Name</th>
                        <th>Score</th>
                        <th>Percentage</th>
                        <th>Exam Date</th>
                        <th>Subject</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>

                <tbody>

                    {% for student in students %}

                    <tr>

                        <td>{{ (page-1)*10 + loop.index }}</td>

                        <td>{{ student.roll_number }}</td>

                        <td>

                            <img
                                src="{{ url_for('static', filename='uploads/' ~ (student.photo or 'default.jpg')) }}"
                                alt="Student Photo"
                                width="45"
                                height="45"
                                class="rounded-circle me-2"
                                style="object-fit: cover;">

                            {{ student.student_name }}

                        </td>

                        <td>{{ student.score }}</td>

                        <td>{{ student.percentage }}%</td>

                        <td>{{ student.exam_date }}</td>

                        <td>{{ student.subject_name }}</td>

                        <td>

                            {% if student.percentage >= 40 %}

                                <span class="badge bg-success">
                                    Pass
                                </span>

                            {% else %}

                                <span class="badge bg-danger">
                                    Fail
                                </span>

                            {% endif %}

                        </td>

                        <td>

                            <a href="{{ url_for('get_ai_tip', id=student.id) }}"
                               class="btn btn-info btn-sm mb-1">
                                💡 AI Study Tips
                            </a>

                            {% if session.get("role") == "admin" %}

                                <a href="{{ url_for('edit_student', roll_number=student.roll_number) }}"
                                   class="btn btn-warning btn-sm mb-1">
                                    Update
                                </a>

                                <form
                                    method="POST"
                                    action="{{ url_for('delete_student', roll_number=student.roll_number) }}"
                                    style="display:inline;">

                                    <button
                                        type="submit"
                                        class="btn btn-danger btn-sm"
                                        onclick="return confirm('Are you sure you want to delete this student?')">

                                        Delete

                                    </button>

                                </form>

                            {% endif %}

                        </td>

                    </tr>

                    {% endfor %}

                </tbody>

            </table>

            <!-- Pagination -->

            <nav class="mt-4">
                <ul class="pagination justify-content-center">

                    {% if page > 1 %}
                    <li class="page-item">
                        <a class="page-link"
                           href="{{ url_for('records', page=page-1, status=request.args.get('status')) }}">
                            Previous
                        </a>
                    </li>
                    {% endif %}

                    {% for p in range(1, total_pages + 1) %}
                    <li class="page-item {% if p == page %}active{% endif %}">
                        <a class="page-link"
                           href="{{ url_for('records', page=p, status=request.args.get('status')) }}">
                            {{ p }}
                        </a>
                    </li>
                    {% endfor %}

                    {% if page < total_pages %}
                    <li class="page-item">
                        <a class="page-link"
                           href="{{ url_for('records', page=page+1, status=request.args.get('status')) }}">
                            Next
                        </a>
                    </li>
                    {% endif %}

                </ul>
            </nav>

        </div>

        <!-- Statistics Card -->

        <div class="col-md-4">

            <div class="card shadow">

                <div class="card-body">

                    <h4 class="text-center">
                        📊 Statistics
                    </h4>

                    <hr>

                    <p>
                        <strong>Total Students:</strong>
                        {{ total_students }}
                    </p>

                    <p>
                        <strong>Passed Students:</strong>
                        {{ passed_students }}
                    </p>

                    <p>
                        <strong>Failed Students:</strong>
                        {{ failed_students }}
                    </p>

                    {% if tip %}

                        <hr>

                        <h5>
                            💡 AI Study Tip
                        </h5>

                        <div class="alert alert-info">
                            {{ tip }}
                        </div>

                    {% endif %}

                </div>

            </div>

        </div>

    </div>

</div>

{% endblock %}'''

home.html
{% extends "base.html" %}

{% block title %}
Smart Exam Portal | Dashboard
{% endblock %}

{% block content %}

<style>

    /* ==============================
       HOME DASHBOARD
    ============================== */

    .dashboard-wrapper {
        padding: 10px 0 30px;
    }


    /* ==============================
       WELCOME BANNER
    ============================== */

    .welcome-banner {
        position: relative;
        overflow: hidden;

        background: linear-gradient(
            135deg,
            #1e3a8a,
            #4f46e5,
            #7c3aed
        );

        color: white;
        border-radius: 24px;

        padding: 35px;

        margin-bottom: 25px;

        box-shadow:
            0 12px 30px rgba(79, 70, 229, 0.20);
    }


    .welcome-banner::before {
        content: "";
        position: absolute;

        width: 180px;
        height: 180px;

        border-radius: 50%;

        background: rgba(255,255,255,0.08);

        right: 80px;
        top: -80px;
    }


    .welcome-banner::after {
        content: "";
        position: absolute;

        width: 120px;
        height: 120px;

        border-radius: 50%;

        background: rgba(255,255,255,0.06);

        right: -30px;
        bottom: -40px;
    }


    .welcome-content {
        position: relative;
        z-index: 2;
    }


    .welcome-badge {
        display: inline-block;

        background: rgba(255,255,255,0.15);

        padding: 7px 14px;

        border-radius: 20px;

        font-size: 13px;

        margin-bottom: 12px;
    }


    .welcome-title {
        font-size: 32px;
        font-weight: 700;

        margin-bottom: 8px;
    }


    .welcome-text {
        max-width: 650px;

        opacity: 0.90;

        margin-bottom: 22px;
    }


    .dashboard-btn {
        border-radius: 11px;

        padding: 10px 18px;

        font-weight: 600;

        transition: 0.3s ease;
    }


    .dashboard-btn:hover {
        transform: translateY(-2px);
    }


    .welcome-icon {
        position: relative;
        z-index: 2;

        font-size: 85px;

        text-align: center;
    }


    /* ==============================
       STATISTICS
    ============================== */

    .stat-card {
        border: none;

        border-radius: 18px;

        height: 100%;

        background: white;

        box-shadow:
            0 5px 20px rgba(0,0,0,0.06);

        transition: 0.3s ease;

        overflow: hidden;
    }


    .stat-card:hover {
        transform: translateY(-5px);

        box-shadow:
            0 12px 25px rgba(0,0,0,0.10);
    }


    .stat-card-body {
        padding: 22px;
    }


    .stat-top {
        display: flex;

        align-items: center;

        justify-content: space-between;

        margin-bottom: 18px;
    }


    .stat-icon {
        width: 50px;
        height: 50px;

        border-radius: 14px;

        display: flex;

        align-items: center;
        justify-content: center;

        font-size: 23px;
    }


    .stat-label {
        color: #6b7280;

        font-size: 14px;

        font-weight: 500;
    }


    .stat-value {
        font-size: 30px;

        font-weight: 700;

        margin: 0;
    }


    .stat-description {
        color: #9ca3af;

        font-size: 12px;

        margin-top: 5px;
    }


    .icon-blue {
        background: #dbeafe;
    }


    .icon-green {
        background: #dcfce7;
    }


    .icon-red {
        background: #fee2e2;
    }


    .icon-purple {
        background: #ede9fe;
    }


    .icon-orange {
        background: #fef3c7;
    }


    /* ==============================
       SECTION CARD
    ============================== */

    .dashboard-card {
        border: none;

        border-radius: 20px;

        background: white;

        box-shadow:
            0 5px 20px rgba(0,0,0,0.06);

        height: 100%;
    }


    .dashboard-card-header {
        padding: 20px 22px 10px;

        display: flex;

        align-items: center;

        justify-content: space-between;
    }


    .dashboard-card-title {
        font-size: 18px;

        font-weight: 700;

        color: #1f2937;

        margin: 0;
    }


    .dashboard-card-subtitle {
        color: #9ca3af;

        font-size: 12px;

        margin-top: 4px;
    }


    /* ==============================
       PERFORMANCE OVERVIEW
    ============================== */

    .performance-box {
        padding: 15px 22px 22px;
    }


    .performance-row {
        margin-bottom: 18px;
    }


    .performance-label {
        display: flex;

        justify-content: space-between;

        margin-bottom: 7px;

        font-size: 13px;

        font-weight: 600;
    }


    .progress {
        height: 9px;

        border-radius: 20px;

        background: #eef1f7;
    }


    .progress-bar {
        border-radius: 20px;
    }


    .pass-bar {
        background: #16a34a;
    }


    .fail-bar {
        background: #ef4444;
    }


    /* ==============================
       QUICK ACTIONS
    ============================== */

    .quick-action {
        display: flex;

        align-items: center;

        gap: 14px;

        padding: 15px;

        margin: 0 22px 12px;

        border: 1px solid #edf0f5;

        border-radius: 13px;

        text-decoration: none;

        color: #1f2937;

        transition: 0.25s ease;
    }


    .quick-action:hover {
        transform: translateX(4px);

        border-color: #c7d2fe;

        background: #f8f9ff;

        color: #1f2937;
    }


    .quick-icon {
        width: 42px;
        height: 42px;

        border-radius: 11px;

        display: flex;

        align-items: center;
        justify-content: center;

        font-size: 19px;
    }


    .quick-title {
        font-weight: 600;

        font-size: 14px;
    }


    .quick-description {
        color: #9ca3af;

        font-size: 12px;
    }


    /* ==============================
       FEATURES
    ============================== */

    .feature-item {
        display: flex;

        align-items: center;

        gap: 13px;

        padding: 13px 22px;

        border-bottom: 1px solid #eef0f5;
    }


    .feature-item:last-child {
        border-bottom: none;
    }


    .feature-icon {
        width: 38px;
        height: 38px;

        border-radius: 10px;

        background: #eef2ff;

        display: flex;

        align-items: center;
        justify-content: center;

        font-size: 17px;

        flex-shrink: 0;
    }


    .feature-title {
        font-size: 14px;

        font-weight: 600;
    }


    .feature-text {
        color: #9ca3af;

        font-size: 12px;

        margin-top: 2px;
    }


    /* ==============================
       RESPONSIVE
    ============================== */

    @media (max-width: 768px) {

        .dashboard-wrapper {
            padding-top: 5px;
        }

        .welcome-banner {
            padding: 28px 22px;

            text-align: center;
        }

        .welcome-title {
            font-size: 26px;
        }

        .welcome-icon {
            font-size: 55px;

            margin-top: 20px;
        }

    }

</style>


<div class="container-fluid dashboard-wrapper">


    <!-- =================================
         WELCOME BANNER
    ================================== -->

    <div class="welcome-banner">

        <div class="row align-items-center">

            <div class="col-lg-8">

                <div class="welcome-content">

                    <span class="welcome-badge">
                        🎓 Online Examination System
                    </span>

                    <h1 class="welcome-title">
                        Welcome to Smart Exam Portal
                    </h1>

                    <p class="welcome-text">
                        Manage online MCQ examinations, students,
                        results and academic performance from one
                        simple platform.
                    </p>


                    <div class="d-flex flex-wrap gap-2">

                        <a
                            href="{{ url_for('exam') }}"
                            class="btn btn-light dashboard-btn">

                            📝 Start Exam

                        </a>


                        <a
                            href="{{ url_for('records') }}"
                            class="btn btn-outline-light dashboard-btn">

                            👨‍🎓 View Students

                        </a>

                    </div>

                </div>

            </div>


            <div class="col-lg-4">

                <div class="welcome-icon">
                    🖥️
                </div>

            </div>

        </div>

    </div>



    <!-- =================================
         STATISTICS
    ================================== -->

    <div class="row g-4 mb-4">


        <!-- Total Students -->

        <div class="col-xl-3 col-md-6">

            <div class="card stat-card">

                <div class="stat-card-body">

                    <div class="stat-top">

                        <div class="stat-icon icon-blue">
                            👨‍🎓
                        </div>

                    </div>


                    <div class="stat-label">
                        Total Students
                    </div>

                    <p class="stat-value text-primary">
                        {{ passed_students + failed_students }}
                    </p>

                    <div class="stat-description">
                        Total examination records
                    </div>

                </div>

            </div>

        </div>


        <!-- Passed -->

        <div class="col-xl-3 col-md-6">

            <div class="card stat-card">

                <div class="stat-card-body">

                    <div class="stat-top">

                        <div class="stat-icon icon-green">
                            ✅
                        </div>

                    </div>


                    <div class="stat-label">
                        Passed Students
                    </div>

                    <p class="stat-value text-success">
                        {{ passed_students }}
                    </p>

                    <div class="stat-description">
                        Students who passed
                    </div>

                </div>

            </div>

        </div>


        <!-- Failed -->

        <div class="col-xl-3 col-md-6">

            <div class="card stat-card">

                <div class="stat-card-body">

                    <div class="stat-top">

                        <div class="stat-icon icon-red">
                            ❌
                        </div>

                    </div>


                    <div class="stat-label">
                        Failed Students
                    </div>

                    <p class="stat-value text-danger">
                        {{ failed_students }}
                    </p>

                    <div class="stat-description">
                        Students who need improvement
                    </div>

                </div>

            </div>

        </div>


        <!-- Average -->

        <div class="col-xl-3 col-md-6">

            <div class="card stat-card">

                <div class="stat-card-body">

                    <div class="stat-top">

                        <div class="stat-icon icon-purple">
                            📊
                        </div>

                    </div>


                    <div class="stat-label">
                        Average Score
                    </div>

                    <p class="stat-value text-primary">
                        {{ average_score|round(2) }}
                    </p>

                    <div class="stat-description">
                        Overall average performance
                    </div>

                </div>

            </div>

        </div>

    </div>



    <!-- =================================
         SECOND ROW
    ================================== -->

    <div class="row g-4 mb-4">


        <!-- PERFORMANCE -->

        <div class="col-lg-7">

            <div class="card dashboard-card">

                <div class="dashboard-card-header">

                    <div>

                        <h4 class="dashboard-card-title">
                            📈 Performance Overview
                        </h4>

                        <div class="dashboard-card-subtitle">
                            Current student result distribution
                        </div>

                    </div>

                    <span class="badge bg-primary-subtle text-primary">
                        Results
                    </span>

                </div>


                <div class="performance-box">


                    <!-- Pass -->

                    <div class="performance-row">

                        <div class="performance-label">

                            <span>
                                ✅ Passed Students
                            </span>

                            <span>
                                {{ passed_students }}
                            </span>

                        </div>

                        <div class="progress">

                            {% set total =
                                passed_students + failed_students %}

                            {% if total > 0 %}

                                {% set pass_percent =
                                    (passed_students / total * 100) %}

                            {% else %}

                                {% set pass_percent = 0 %}

                            {% endif %}

                            <div
                                class="progress-bar pass-bar"
                                style="width: {{ pass_percent }}%;">

                            </div>

                        </div>

                    </div>


                    <!-- Fail -->

                    <div class="performance-row">

                        <div class="performance-label">

                            <span>
                                ❌ Failed Students
                            </span>

                            <span>
                                {{ failed_students }}
                            </span>

                        </div>

                        <div class="progress">

                            {% if total > 0 %}

                                {% set fail_percent =
                                    (failed_students / total * 100) %}

                            {% else %}

                                {% set fail_percent = 0 %}

                            {% endif %}

                            <div
                                class="progress-bar fail-bar"
                                style="width: {{ fail_percent }}%;">

                            </div>

                        </div>

                    </div>


                    <!-- Highest Score -->

                    <div class="mt-4 p-3 rounded-3 bg-light">

                        <div class="d-flex justify-content-between
                                    align-items-center">

                            <div>

                                <div class="text-muted small">
                                    🏆 Highest Score
                                </div>

                                <strong class="fs-4">
                                    {{ highest_score }}
                                </strong>

                            </div>

                            <div class="fs-1">
                                🏆
                            </div>

                        </div>

                    </div>

                </div>

            </div>

        </div>



        <!-- QUICK ACTIONS -->

        <div class="col-lg-5">

            <div class="card dashboard-card">

                <div class="dashboard-card-header">

                    <div>

                        <h4 class="dashboard-card-title">
                            ⚡ Quick Actions
                        </h4>

                        <div class="dashboard-card-subtitle">
                            Frequently used options
                        </div>

                    </div>

                </div>


                <div class="pt-2 pb-2">


                    <!-- Start Exam -->

                    <a
                        href="{{ url_for('exam') }}"
                        class="quick-action">

                        <div class="quick-icon icon-blue">
                            📝
                        </div>

                        <div>

                            <div class="quick-title">
                                Start New Exam
                            </div>

                            <div class="quick-description">
                                Begin an online MCQ examination
                            </div>

                        </div>

                    </a>


                    <!-- Records -->

                    <a
                        href="{{ url_for('records') }}"
                        class="quick-action">

                        <div class="quick-icon icon-purple">
                            👨‍🎓
                        </div>

                        <div>

                            <div class="quick-title">
                                Manage Students
                            </div>

                            <div class="quick-description">
                                View student records and results
                            </div>

                        </div>

                    </a>


                    <!-- Add Student -->

                    {% if session.get('role') == 'admin' %}

                    <a
                        href="{{ url_for('add_students') }}"
                        class="quick-action">

                        <div class="quick-icon icon-green">
                            ➕
                        </div>

                        <div>

                            <div class="quick-title">
                                Add Student
                            </div>

                            <div class="quick-description">
                                Register a new student
                            </div>

                        </div>

                    </a>

                    {% endif %}


                </div>

            </div>

        </div>

    </div>



    <!-- =================================
         FEATURES + HIGHEST SCORE
    ================================== -->

    <div class="row g-4">


        <!-- PORTAL FEATURES -->

        <div class="col-lg-8">

            <div class="card dashboard-card">

                <div class="dashboard-card-header">

                    <div>

                        <h4 class="dashboard-card-title">
                            🚀 Portal Features
                        </h4>

                        <div class="dashboard-card-subtitle">
                            Smart tools available in your examination portal
                        </div>

                    </div>

                </div>


                <div class="feature-item">

                    <div class="feature-icon">
                        📝
                    </div>

                    <div>

                        <div class="feature-title">
                            Online MCQ Tests
                        </div>

                        <div class="feature-text">
                            Conduct multiple-choice online examinations.
                        </div>

                    </div>

                </div>


                <div class="feature-item">

                    <div class="feature-icon">
                        👨‍🎓
                    </div>

                    <div>

                        <div class="feature-title">
                            Student Records
                        </div>

                        <div class="feature-text">
                            Manage and track student examination records.
                        </div>

                    </div>

                </div>


                <div class="feature-item">

                    <div class="feature-icon">
                        🎯
                    </div>

                    <div>

                        <div class="feature-title">
                            Automatic Score Calculation
                        </div>

                        <div class="feature-text">
                            Calculate examination marks automatically.
                        </div>

                    </div>

                </div>


                <div class="feature-item">

                    <div class="feature-icon">
                        📊
                    </div>

                    <div>

                        <div class="feature-title">
                            Percentage Calculation
                        </div>

                        <div class="feature-text">
                            Automatically calculate student percentage.
                        </div>

                    </div>

                </div>


                <div class="feature-item">

                    <div class="feature-icon">
                        🏆
                    </div>

                    <div>

                        <div class="feature-title">
                            Pass / Fail Result
                        </div>

                        <div class="feature-text">
                            Quickly identify examination performance.
                        </div>

                    </div>

                </div>

            </div>

        </div>



        <!-- SUMMARY -->

        <div class="col-lg-4">

            <div class="card dashboard-card">

                <div class="dashboard-card-header">

                    <div>

                        <h4 class="dashboard-card-title">
                            📌 Result Summary
                        </h4>

                        <div class="dashboard-card-subtitle">
                            Quick examination overview
                        </div>

                    </div>

                </div>


                <div class="p-4">


                    <div class="d-flex justify-content-between
                                align-items-center mb-3">

                        <span class="text-muted">
                            Total Records
                        </span>

                        <strong>
                            {{ passed_students + failed_students }}
                        </strong>

                    </div>


                    <div class="d-flex justify-content-between
                                align-items-center mb-3">

                        <span class="text-muted">
                            Passed
                        </span>

                        <span class="badge bg-success">
                            {{ passed_students }}
                        </span>

                    </div>


                    <div class="d-flex justify-content-between
                                align-items-center mb-3">

                        <span class="text-muted">
                            Failed
                        </span>

                        <span class="badge bg-danger">
                            {{ failed_students }}
                        </span>

                    </div>


                    <div class="d-flex justify-content-between
                                align-items-center mb-4">

                        <span class="text-muted">
                            Highest Score
                        </span>

                        <span class="badge bg-warning text-dark">
                            {{ highest_score }}
                        </span>

                    </div>


                    <a
                        href="{{ url_for('records') }}"
                        class="btn btn-primary w-100 dashboard-btn">

                        📊 View Complete Results

                    </a>

                </div>

            </div>

        </div>

    </div>



    <!-- FOOTER -->

    <div class="text-center text-muted mt-4 mb-2">

        🎓 <strong>Smart Exam Portal</strong>

        <br>

        <small>
            Online Examination & Student Performance Management System
        </small>

    </div>


</div>

{% endblock %}

#home page
{% extends "base.html" %}

{% block content %}

<style>
    .hero-section {
        background: linear-gradient(135deg, #0d6efd, #6610f2);
        color: white;
        border-radius: 20px;
        padding: 40px;
        margin-bottom: 30px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }

    .hero-section h1 {
        font-weight: 700;
    }

    .hero-section p {
        font-size: 17px;
        opacity: 0.95;
    }

    .stat-card {
        border: none;
        border-radius: 18px;
        transition: 0.3s;
        height: 100%;
    }

    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.12);
    }

    .stat-icon {
        width: 55px;
        height: 55px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 26px;
        margin-bottom: 15px;
    }

    .icon-blue {
        background: #e7f1ff;
    }

    .icon-green {
        background: #e8f8ef;
    }

    .icon-red {
        background: #fdeaea;
    }

    .icon-purple {
        background: #f0e9ff;
    }

    .icon-orange {
        background: #fff0df;
    }

    .stat-title {
        color: #6c757d;
        font-size: 15px;
        font-weight: 600;
    }

    .stat-number {
        font-size: 30px;
        font-weight: 700;
        margin: 5px 0;
    }

    .section-card {
        border: none;
        border-radius: 18px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    }

    .feature-box {
        padding: 20px;
        border-radius: 15px;
        background: #f8f9fa;
        height: 100%;
    }

    .feature-box h5 {
        font-weight: 600;
    }

    .quick-btn {
        border-radius: 12px;
        padding: 12px 20px;
        font-weight: 600;
    }
</style>


<div class="container py-4">

    <!-- ========================= -->
    <!-- HERO SECTION -->
    <!-- ========================= -->

    <div class="hero-section">

        <h1>🎓 Welcome to Smart Exam Portal</h1>

        <p class="mb-0">
            Manage students, conduct online exams,
            and view examination results easily.
        </p>

    </div>


    <!-- ========================= -->
    <!-- STATISTICS -->
    <!-- ========================= -->

    <div class="row g-4 mb-4">

        <!-- Total Attempts -->
        <div class="col-lg col-md-6">
            <div class="card stat-card shadow-sm">

                <div class="card-body p-4">

                    <div class="stat-icon icon-blue">
                        👥
                    </div>

                    <div class="stat-title">
                        Total Attempts
                    </div>

                    <div class="stat-number text-primary">
                        {{ total_attempts }}
                    </div>

                </div>

            </div>
        </div>


        <!-- Passed Students -->
        <div class="col-lg col-md-6">
            <div class="card stat-card shadow-sm">

                <div class="card-body p-4">

                    <div class="stat-icon icon-green">
                        ✅
                    </div>

                    <div class="stat-title">
                        Passed Students
                    </div>

                    <div class="stat-number text-success">
                        {{ passed_students }}
                    </div>

                </div>

            </div>
        </div>


        <!-- Failed Students -->
        <div class="col-lg col-md-6">
            <div class="card stat-card shadow-sm">

                <div class="card-body p-4">

                    <div class="stat-icon icon-red">
                        ❌
                    </div>

                    <div class="stat-title">
                        Failed Students
                    </div>

                    <div class="stat-number text-danger">
                        {{ failed_students }}
                    </div>

                </div>

            </div>
        </div>


        <!-- Average Score -->
        <div class="col-lg col-md-6">
            <div class="card stat-card shadow-sm">

                <div class="card-body p-4">

                    <div class="stat-icon icon-purple">
                        📊
                    </div>

                    <div class="stat-title">
                        Average Score
                    </div>

                    <div class="stat-number text-purple">
                        {{ "%.1f"|format(average_score) }}
                    </div>

                </div>

            </div>
        </div>


        <!-- Highest Score -->
        <div class="col-lg col-md-6">
            <div class="card stat-card shadow-sm">

                <div class="card-body p-4">

                    <div class="stat-icon icon-orange">
                        🏆
                    </div>

                    <div class="stat-title">
                        Highest Score
                    </div>

                    <div class="stat-number text-warning">
                        {{ highest_score }}
                    </div>

                </div>

            </div>
        </div>


        <!-- Available Exams -->
        <div class="col-lg col-md-6">
            <div class="card stat-card shadow-sm">

                <div class="card-body p-4">

                    <div class="stat-icon icon-blue">
                        📝
                    </div>

                    <div class="stat-title">
                        Available Exams
                    </div>

                    <div class="stat-number text-primary">
                        {{ available_exams }}
                    </div>

                    <a href="{{ url_for('available_exams') }}"
                       class="btn btn-primary btn-sm mt-2">
                        View Exams
                    </a>

                </div>

            </div>
        </div>

    </div>


    <!-- ========================= -->
    <!-- FEATURES -->
    <!-- ========================= -->

    <div class="card section-card mb-4">

        <div class="card-body p-4">

            <h3 class="mb-4">
                🚀 Portal Features
            </h3>

            <div class="row g-4">

                <div class="col-md-4">
                    <div class="feature-box">

                        <h5>📝 Online Exams</h5>

                        <p class="text-muted mb-0">
                            Conduct MCQ based online examinations
                            in an easy and organized way.
                        </p>

                    </div>
                </div>


                <div class="col-md-4">
                    <div class="feature-box">

                        <h5>👨‍🎓 Student Management</h5>

                        <p class="text-muted mb-0">
                            Add, update, search and manage
                            student examination records.
                        </p>

                    </div>
                </div>


                <div class="col-md-4">
                    <div class="feature-box">

                        <h5>📊 Results & Scores</h5>

                        <p class="text-muted mb-0">
                            Automatically calculate scores,
                            percentage and pass/fail status.
                        </p>

                    </div>
                </div>

            </div>

        </div>

    </div>


    <!-- ========================= -->
    <!-- QUICK ACTIONS -->
    <!-- ========================= -->

    <div class="card section-card">

        <div class="card-body p-4">

            <h3 class="mb-4">
                ⚡ Quick Actions
            </h3>

            <div class="d-flex flex-wrap gap-3">

                <a href="{{ url_for('available_exams') }}"
                   class="btn btn-primary quick-btn">
                    📝 Available Exams
                </a>

                <a href="{{ url_for('records') }}"
                   class="btn btn-outline-primary quick-btn">
                    📋 View Records
                </a>

                {% if session.get("role") == "admin" %}

                <a href="{{ url_for('create_exam') }}"
                   class="btn btn-success quick-btn">
                    ➕ Create Exam
                </a>

                {% endif %}

            </div>

        </div>

    </div>

</div>

{% endblock %}