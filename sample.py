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