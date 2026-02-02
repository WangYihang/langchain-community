
import pytest
from langchain_core.agents import AgentAction, AgentFinish
from langchain_community.agent_toolkits.openapi.planner import RobustOpenAPIPlannerOutputParser

def test_robust_parser_standard_action():
    parser = RobustOpenAPIPlannerOutputParser()
    text = "Thought: I should do this\nAction: test_tool\nAction Input: test_input"
    result = parser.parse(text)
    assert isinstance(result, AgentAction)
    assert result.tool == "test_tool"
    assert result.tool_input == "test_input"

def test_robust_parser_final_answer():
    parser = RobustOpenAPIPlannerOutputParser()
    text = "Thought: I am done\nFinal Answer: The result is 42"
    result = parser.parse(text)
    assert isinstance(result, AgentFinish)
    assert result.return_values["output"] == "The result is 42"

def test_robust_parser_malformed_missing_action():
    parser = RobustOpenAPIPlannerOutputParser()
    # This simulates the error case: The model just outputs text without Action or Final Answer
    text = "Based on the API response, the weather is sunny."
    result = parser.parse(text)
    assert isinstance(result, AgentFinish)
    # The whole text should be the output
    assert result.return_values["output"] == "Based on the API response, the weather is sunny."

def test_robust_parser_thought_only():
    parser = RobustOpenAPIPlannerOutputParser()
    text = "Thought: I am thinking..."
    # Even if it just thinks, if it stops, we might as well return it as finish or it's a incomplete generation.
    # But our logic falls back to Finish.
    result = parser.parse(text)
    assert isinstance(result, AgentFinish)
    assert result.return_values["output"] == "Thought: I am thinking..."
