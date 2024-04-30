import cProfile
import pstats
import uvicorn
from app.main import app as project

if __name__ == "__main__":
    cProfile.run(
        "uvicorn.run(project, host='0.0.0.0', port=8000)",
        filename="profile_results.prof",
    )

    p = pstats.Stats("profile_results.prof")
    p.strip_dirs().sort_stats(-1).print_stats()
