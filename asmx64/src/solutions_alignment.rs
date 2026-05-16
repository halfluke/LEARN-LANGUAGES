#[cfg(test)]
mod tests {
    use crate::chapter::{ChapterLoader, default_chapters_dir};
    use crate::executor::Executor;
    use crate::validator::Validator;

    #[test]
    #[ignore = "slow: full chapter matrix; enabled in verify-all"]
    fn reference_solutions_pass_via_tui_executor() {
        if std::env::var("SKIP_SOLUTION_ALIGNMENT").as_deref() == Ok("1") {
            return;
        }

        let loader = ChapterLoader::new(default_chapters_dir());
        let chapters = loader.load_chapters().expect("load chapters");
        let executor = Executor::new();
        let validator = Validator::new();

        for ch in &chapters {
            for ex in &ch.exercises {
                if ex.solution.trim().is_empty() {
                    continue;
                }
                let res = executor
                    .execute_code(&ex.solution)
                    .unwrap_or_else(|e| panic!("{}::{} execute: {e}", ch.id, ex.id));
                let v = validator.validate(&res, ex, 0);
                assert!(v.passed, "{}::{}: {}", ch.id, ex.id, v.message);
            }
        }
    }
}
