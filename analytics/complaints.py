def detect_issue(review):

    review = str(review).lower()

    # LOGIN
    if any(word in review for word in [
        "login",
        "otp",
        "signin",
        "sign in",
        "password"
    ]):
        return "Login Issue"

    # CRASH
    elif any(word in review for word in [
        "crash",
        "hang",
        "stuck",
        "freeze",
        "bug"
    ]):
        return "App Crash"

    # SPEED
    elif any(word in review for word in [
        "slow",
        "lag",
        "loading",
        "delay"
    ]):
        return "Performance Issue"

    # UI
    elif any(word in review for word in [
        "ui",
        "design",
        "interface"
    ]):
        return "UI/UX Issue"

    # TRANSACTION
    elif any(word in review for word in [
        "payment",
        "transaction",
        "withdraw",
        "deposit"
    ]):
        return "Transaction Issue"

    # SUPPORT
    elif any(word in review for word in [
        "support",
        "service",
        "customer care"
    ]):
        return "Support Issue"

    else:
        return "Other"
