branch_coverage = {}

def initialize_coverage(func_name, num_branches):
    branch_coverage[func_name] = [False] * num_branches

def mark_branch(func_name, branch_id):
    branch_coverage[func_name][branch_id] = True

def report_coverage():
    total_branches = 0
    reached_branches = 0
    
    for func_name, branches in branch_coverage.items():
        func_total = len(branches)
        func_reached = sum(branches)
        
        total_branches += func_total
        reached_branches += func_reached
        
        coverage_percentage = (func_reached / func_total) * 100 if func_total > 0 else 0
        
        print(f"Coverage for {func_name}:")
        for i, reached in enumerate(branches):
            print(f"  Branch {i}: {'Reached! ✅' if reached else 'Not Reached ❌'}")
        print(f"  Function coverage: {coverage_percentage:.2f}%\n")
    
    overall_coverage = (reached_branches / total_branches) * 100 if total_branches > 0 else 0
    print(f"Overall branch coverage: {overall_coverage:.2f}%")