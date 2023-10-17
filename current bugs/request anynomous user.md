edx-platform/lms/djangoapps/feedback/views.py

function `def index`:

line ~ 52

```python
context = {
    'email': request.user.email # có thể là anynomous user > error
}
```

