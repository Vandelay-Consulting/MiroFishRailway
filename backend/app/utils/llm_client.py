"""
LLM Client Wrapper
Unified OpenAI-format API calls
"""

import json
import re
from typing import Optional, Dict, Any, List
from openai import OpenAI

from ..config import Config


class LLMClient:
    """LLM Client"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
    ):
        self.api_key = api_key or Config.LLM_API_KEY
        self.base_url = base_url or Config.LLM_BASE_URL
        self.model = model or Config.LLM_MODEL_NAME

        if not self.api_key:
            raise ValueError("LLM_API_KEY not configured")

        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format: Optional[Dict] = None,
    ) -> str:
        """
        Send a chat request

        Args:
            messages: Message list
            temperature: Temperature parameter
            max_tokens: Maximum token count
            response_format: Response format (e.g., JSON mode)

        Returns:
            Model response text
        """
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if response_format:
            kwargs["response_format"] = response_format

        response = self.client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content
        # Some models (e.g., MiniMax M2.5) include <think> content in response, need to remove
        content = re.sub(r"<think>[\s\S]*?</think>", "", content).strip()
        return content

    def chat_json(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 4096,
    ) -> Dict[str, Any]:
        """
        Send a chat request and return JSON

        Args:
            messages: Message list
            temperature: Temperature parameter
            max_tokens: Maximum token count

        Returns:
            Parsed JSON object
        """
        response = self.chat(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        # Clean up markdown code block markers
        cleaned_response = response.strip()
        # Remove think tags (MiniMax and similar models)
        cleaned_response = re.sub(
            r"<think>[\s\S]*?</think>", "", cleaned_response, flags=re.IGNORECASE
        )
        cleaned_response = re.sub(
            r"^```(?:json)?\s*\n?", "", cleaned_response, flags=re.IGNORECASE
        )
        cleaned_response = re.sub(r"\n?```\s*$", "", cleaned_response)
        cleaned_response = cleaned_response.strip()

        # If response is empty
        if not cleaned_response:
            raise ValueError("LLM returned an empty response")

        # Try to parse JSON, attempt repair if failed
        try:
            return json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            # Try to fix common LLM JSON errors
            repaired = self._repair_json(cleaned_response)
            try:
                return json.loads(repaired)
            except json.JSONDecodeError:
                # Repair failed, raise original error
                raise ValueError(f"LLM returned invalid JSON format: {cleaned_response}")

    def _repair_json(self, text: str) -> str:
        """
        Attempt to repair common LLM JSON errors

        Issues fixed:
        1. Duplicate attributes arrays (first string array, then object array)
        2. Extra commas
        3. Missing quotes
        4. Trailing commas
        """

        # Fix 1: Handle duplicate array issue in attributes field
        # Pattern: "attributes": ["a", "b"],\n[\n {...}, {...}\n]
        # Should become: "attributes": [\n {...}, {...}\n]
        def fix_duplicate_attributes(match):
            # Keep the second array (object array), discard the first (string array)
            return '"attributes":' + match.group(2)

        # Match "attributes": [...],\n[...] pattern (two consecutive arrays)
        pattern = r'"attributes"\s*:\s*(\[[^\]]*\])\s*,?\s*([\s\S]*?\])'
        text = re.sub(pattern, fix_duplicate_attributes, text)

        # Fix 2: Remove trailing commas after last element in objects/arrays
        text = re.sub(r",(\s*[}\]])", r"\1", text)

        # Fix 3: Fix single quotes (replace with double quotes)
        text = re.sub(r"'([^']*)'(?=\s*:)", r'"\1"', text)  # Key names
        text = re.sub(r":\s*'([^']*)'", r': "\1"', text)  # String values

        # Fix 4: Fix missing commas (add comma before key on new line)
        text = re.sub(r'(\S)\s*\n\s*"', r'\1,\n"', text)

        return text
