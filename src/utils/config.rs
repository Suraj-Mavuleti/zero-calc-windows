pub struct AppConfig { pub debug_mode: bool }
impl AppConfig { pub fn load() -> Self { AppConfig { debug_mode: false } } }
