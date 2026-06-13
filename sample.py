<!DOCTYPE html>
<html>
<head>
    <title>Smart Exam Portal</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
.search-btn{
    transition: all 0.3s ease;
}

.search-btn:hover{
    transform: translateY(-2px);
    box-shadow: 0 4px 10px #e7e1e14d;
}

.navbar-brand{
    font-size: 28px;
    font-weight: bold;
}

.nav-link{
    font-weight: 500;
}

.nav-link:hover{
    color: rgb(241, 241, 25) !important;
}
</style>
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container">
        <a class="navbar-brand" href="{{ url_for('home') }}">
            🎓 Smart Exam Portal
        </a>

        <div>
            <a class="nav-link text-white d-inline" href="{{ url_for('home') }}">🏠Home</a>
            <a class="nav-link text-white d-inline" href="{{ url_for('records') }}">📚Records</a>
            <a class="nav-link text-white d-inline" href="{{ url_for('add_students') }}">👨‍🎓Add Student</a>
            <a class="nav-link text-white d-inline" href="{{ url_for('exam') }}">📝Start Exam</a>
            <form class="d-flex ms-3" action="{{url_for('search')}}" method="GET">
    
    <input class="form-control me-2 rounded-pill"
           type="search"
           placeholder="🔍 Search Student"
           name="q"
           style="width:180px;">

    <button class="btn btn-warning fw-bold rounded-pill px-3 search-btn"
            type="submit">
        Search
    </button>

</form>
        </div>
    </div>
</nav>

<div class="container mt-4">

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

<footer class="bg-dark text-white text-center p-3 mt-5">
    © 2026 Smart Exam Portal
</footer>

</body>
</html>