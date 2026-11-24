from functools import wraps


def trace_call(label):
    def decorator(target_fn):
        @wraps(target_fn)
        def wrapper(*args, **kwargs):
            print(label)
            print("Input:", args)
            outcome = target_fn(*args, **kwargs)
            print("Output:", outcome)
            return outcome
        return wrapper
    return decorator


@trace_call("Adding (no return)")
def sum_without_return(x, y):
    x + y


@trace_call("Adding (return)")
def sum_with_return(x, y):
    return x + y


def run():
    sum_without_return(4, 3)
    print()
    sum_with_return(4, 3)


if __name__ == "__main__":
    run()