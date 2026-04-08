window.GAME_LIST = Object.freeze([
    {
        id: "sudoku",
        title: "数独训练",
        summary: "支持 4x4、6x6、9x9 多种盘面，适合练习数字推理和专注力。",
        href: "./games/sudoku/index.html",
        status: "已接入",
        difficulty: "多难度",
        age: "建议 6+",
        tags: ["逻辑推理", "数字敏感", "专注训练"]
    },
    {
        id: "tic-tac-toe",
        title: "井字棋",
        summary: "支持双人对战和人机模式，适合练习判断、预判和规则理解。",
        href: "./games/tic-tac-toe/index.html",
        status: "已接入",
        difficulty: "轻量策略",
        age: "建议 4+",
        tags: ["规则理解", "回合判断", "策略启蒙"]
    }
]);
