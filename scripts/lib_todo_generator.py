#!/usr/bin/env python3
"""
TODO Generator Library

Generates sprint-based TODO lists for Windsurf projects.
Renamed from todo_generator.py to follow library naming convention.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging


class TODOGenerator:
    """Generates Windsurf-compatible TODO lists for projects."""
    
    def __init__(self):
        self.logger = logging.getLogger('todo_generator')
        self.todo_templates = {
            "game-development": self._get_game_dev_todos(),
            "agentic-ai": self._get_agentic_ai_todos(),
            "data-science": self._get_data_science_todos(),
            "web-api": self._get_web_api_todos(),
            "custom-multi": self._get_custom_todos()
        }

    def generate_todo_file(
        self, 
        project_name: str, 
        template_type: str, 
        sprint_number: int = 1,
        output_dir: Optional[Path] = None,
        custom_requirements: List[str] = None
    ) -> Optional[Path]:
        """
        Generate a TODO file for a specific sprint.
        
        Args:
            project_name: Name of the project
            template_type: Type of TODO template to use
            sprint_number: Sprint number (1-4)
            output_dir: Directory to save the TODO file
            custom_requirements: Additional custom requirements
            
        Returns:
            Path to generated TODO file or None if failed
        """
        try:
            todo_content = self.generate_todo_list(
                template_type, project_name, sprint_number, custom_requirements
            )
            
            if output_dir is None:
                output_dir = Path.cwd()
            
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"TODO.{project_name}.{sprint_number}.md"
            
            output_path.write_text(todo_content, encoding='utf-8')
            self.logger.debug(f"Generated TODO file: {output_path}")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate TODO file: {e}")
            return None

    def generate_todo_list(
        self, 
        template_type: str, 
        project_name: str, 
        sprint_number: int = 1,
        custom_requirements: List[str] = None
    ) -> str:
        """Generate a TODO list for a specific sprint."""
        
        todos = self.todo_templates.get(template_type, {})
        sprint_todos = todos.get(f"sprint_{sprint_number}", [])
        
        # Add custom requirements if provided
        if custom_requirements:
            sprint_todos.append({
                "category": "Custom Requirements", 
                "tasks": [
                    {"task": req, "priority": "medium", "estimated_hours": 2}
                    for req in custom_requirements
                ]
            })
        
        return self._format_windsurf_todo(
            project_name, sprint_number, sprint_todos
        )

    def _format_windsurf_todo(
        self, 
        project_name: str, 
        sprint_number: int, 
        todos: List[Dict[str, Any]]
    ) -> str:
        """Format TODO list in Windsurf-compatible format."""
        
        header = f"""# TODO List: {project_name} - Sprint {sprint_number}

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Sprint Duration:** {datetime.now().strftime('%Y-%m-%d')} to {(datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')}
**Project:** {project_name}

## 📋 Sprint {sprint_number} Objectives

"""
        
        content = ""
        task_counter = 1
        
        for category in todos:
            content += f"## {category['category']}\n\n"
            
            for task in category['tasks']:
                priority_emoji = self._get_priority_emoji(task.get('priority', 'medium'))
                estimated = task.get('estimated_hours', 'TBD')
                
                content += f"- [ ] **{task_counter:02d}.** {priority_emoji} {task['task']}\n"
                if 'description' in task:
                    content += f"  *{task['description']}*\n"
                content += f"  📅 **Estimated:** {estimated}h\n"
                if 'dependencies' in task:
                    content += f"  🔗 **Depends on:** {', '.join(task['dependencies'])}\n"
                content += "\n"
                task_counter += 1
        
        footer = f"""
## 📊 Sprint Metrics

- **Total Tasks:** {task_counter - 1}
- **Estimated Hours:** {self._calculate_total_hours(todos)}
- **High Priority:** {self._count_by_priority(todos, 'high')}
- **Medium Priority:** {self._count_by_priority(todos, 'medium')}
- **Low Priority:** {self._count_by_priority(todos, 'low')}

## 🎯 Definition of Done

- [ ] All tasks completed and tested
- [ ] Code review completed
- [ ] Documentation updated
- [ ] Tests passing (unit + integration)
- [ ] Sprint demo prepared
- [ ] Ready for next sprint

## 📝 Notes

*Add sprint-specific notes, blockers, or important decisions here*

---
**Template:** Windsurf Projects Template Generator v4.0
**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
        
        return header + content + footer

    def _get_priority_emoji(self, priority: str) -> str:
        """Get emoji for task priority."""
        return {
            "high": "🔴",
            "medium": "🟡", 
            "low": "🟢"
        }.get(priority, "🟡")

    def _calculate_total_hours(self, todos: List[Dict[str, Any]]) -> int:
        """Calculate total estimated hours."""
        total = 0
        for category in todos:
            for task in category['tasks']:
                hours = task.get('estimated_hours', 0)
                if isinstance(hours, (int, float)):
                    total += hours
        return total

    def _count_by_priority(self, todos: List[Dict[str, Any]], priority: str) -> int:
        """Count tasks by priority level."""
        count = 0
        for category in todos:
            for task in category['tasks']:
                if task.get('priority') == priority:
                    count += 1
        return count

    def _get_game_dev_todos(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get game development TODO templates."""
        return {
            "sprint_1": [
                {
                    "category": "🏗️ Project Infrastructure",
                    "tasks": [
                        {
                            "task": "Set up Python project structure with Poetry",
                            "description": "Initialize pyproject.toml, create src/ structure",
                            "priority": "high",
                            "estimated_hours": 2
                        },
                        {
                            "task": "Configure development tools (Ruff, MyPy, Pre-commit)",
                            "description": "Set up code quality and formatting tools",
                            "priority": "high", 
                            "estimated_hours": 1
                        },
                        {
                            "task": "Set up testing infrastructure with pytest",
                            "description": "Configure pytest, add basic test structure",
                            "priority": "high",
                            "estimated_hours": 2
                        }
                    ]
                },
                {
                    "category": "🎮 Core Game Engine",
                    "tasks": [
                        {
                            "task": "Initialize pygame and create main game window",
                            "description": "Basic pygame setup with window, event handling",
                            "priority": "high",
                            "estimated_hours": 3
                        },
                        {
                            "task": "Implement basic game loop (update/render cycle)",
                            "description": "Main game loop with FPS control",
                            "priority": "high",
                            "estimated_hours": 2
                        },
                        {
                            "task": "Create game state management system",
                            "description": "Manage game states (menu, playing, paused, game over)",
                            "priority": "medium",
                            "estimated_hours": 3
                        }
                    ]
                }
            ],
            "sprint_2": [
                {
                    "category": "👾 Game Mechanics",
                    "tasks": [
                        {
                            "task": "Implement player spaceship controls",
                            "description": "Keyboard input for movement and shooting",
                            "priority": "high",
                            "estimated_hours": 4
                        },
                        {
                            "task": "Create enemy spawn system",
                            "description": "Generate waves of enemy invaders",
                            "priority": "high",
                            "estimated_hours": 3
                        },
                        {
                            "task": "Implement collision detection",
                            "description": "Bullets hitting enemies, enemies hitting player",
                            "priority": "high",
                            "estimated_hours": 4
                        }
                    ]
                }
            ],
            "sprint_3": [
                {
                    "category": "🎨 Visual & Audio",
                    "tasks": [
                        {
                            "task": "Add sprite graphics for all game objects",
                            "description": "Replace placeholder rectangles with sprites",
                            "priority": "medium",
                            "estimated_hours": 5
                        },
                        {
                            "task": "Implement sound effects and music",
                            "description": "Shooting, explosions, background music",
                            "priority": "medium",
                            "estimated_hours": 3
                        },
                        {
                            "task": "Add particle effects for explosions",
                            "description": "Visual feedback for destroyed enemies",
                            "priority": "low",
                            "estimated_hours": 4
                        }
                    ]
                }
            ],
            "sprint_4": [
                {
                    "category": "🏆 Game Features & Polish",
                    "tasks": [
                        {
                            "task": "Implement scoring system and high scores",
                            "description": "Track player score and save high scores",
                            "priority": "medium",
                            "estimated_hours": 3
                        },
                        {
                            "task": "Add multiple difficulty levels",
                            "description": "Easy, medium, hard modes with different enemy patterns",
                            "priority": "medium",
                            "estimated_hours": 4
                        },
                        {
                            "task": "Create main menu and game over screens",
                            "description": "Navigation between game states",
                            "priority": "high",
                            "estimated_hours": 3
                        }
                    ]
                }
            ]
        }

    def _get_agentic_ai_todos(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get agentic AI TODO templates."""
        return {
            "sprint_1": [
                {
                    "category": "🏗️ Infrastructure Setup",
                    "tasks": [
                        {
                            "task": "Set up crew.ai project structure",
                            "description": "Initialize crew.ai agents and tasks",
                            "priority": "high",
                            "estimated_hours": 3
                        },
                        {
                            "task": "Configure FastAPI with async support",
                            "description": "Create API endpoints for agent interactions",
                            "priority": "high",
                            "estimated_hours": 2
                        },
                        {
                            "task": "Set up Pydantic v2 models",
                            "description": "Define data models for agent inputs/outputs",
                            "priority": "high",
                            "estimated_hours": 2
                        }
                    ]
                },
                {
                    "category": "🤖 Agent Development",
                    "tasks": [
                        {
                            "task": "Create basic research agent",
                            "description": "Agent for information gathering and analysis",
                            "priority": "medium",
                            "estimated_hours": 4
                        },
                        {
                            "task": "Implement writer agent",
                            "description": "Agent for content generation and formatting",
                            "priority": "medium",
                            "estimated_hours": 3
                        }
                    ]
                }
            ]
        }

    def _get_data_science_todos(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get data science TODO templates."""
        return {
            "sprint_1": [
                {
                    "category": "📊 Data Infrastructure",
                    "tasks": [
                        {
                            "task": "Set up Polars for data processing",
                            "description": "Configure high-performance data manipulation",
                            "priority": "high",
                            "estimated_hours": 2
                        },
                        {
                            "task": "Configure DuckDB for analytics",
                            "description": "Set up embedded analytics database",
                            "priority": "high",
                            "estimated_hours": 3
                        }
                    ]
                }
            ]
        }

    def _get_web_api_todos(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get web API TODO templates."""
        return {
            "sprint_1": [
                {
                    "category": "🌐 API Development",
                    "tasks": [
                        {
                            "task": "Set up FastAPI application structure",
                            "description": "Create modular API with routers",
                            "priority": "high",
                            "estimated_hours": 3
                        }
                    ]
                }
            ]
        }

    def _get_custom_todos(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get custom project TODO templates."""
        return {
            "sprint_1": [
                {
                    "category": "🚀 Project Setup",
                    "tasks": [
                        {
                            "task": "Review and customize project requirements",
                            "description": "Analyze specific needs and adapt template",
                            "priority": "high",
                            "estimated_hours": 2
                        }
                    ]
                }
            ]
        }


if __name__ == "__main__":
    # Test functionality
    import argparse
    
    parser = argparse.ArgumentParser(description="TODO Generator Test")
    parser.add_argument("--project-name", required=True, help="Project name")
    parser.add_argument("--template-type", required=True, 
                       choices=["game-development", "agentic-ai", "data-science", "web-api", "custom-multi"],
                       help="Template type")
    parser.add_argument("--sprint", type=int, default=1, help="Sprint number")
    parser.add_argument("--output-dir", type=Path, help="Output directory")
    
    args = parser.parse_args()
    
    generator = TODOGenerator()
    todo_file = generator.generate_todo_file(
        project_name=args.project_name,
        template_type=args.template_type,
        sprint_number=args.sprint,
        output_dir=args.output_dir
    )
    
    if todo_file:
        print(f"✅ Generated TODO file: {todo_file}")
    else:
        print("❌ Failed to generate TODO file")
