# Claude Prompt for Media.net Engineering Project

Copy and paste the following prompt into Claude to generate a top-tier project tailored for your Media.net interview:

***

**Act as a Senior Principal Engineer and Hiring Manager at Media.net.** 

I am applying for a Software Engineering role at Media.net. The role requires strong backend fundamentals (Data Structures, Algorithms, CS fundamentals), experience building high-scale real-time systems, and the ability to responsibly leverage AI/ML and LLMs to improve ad-tech products and engineering workflows.

I need you to design and help me build a "10/10" standout portfolio project that perfectly aligns with this Job Description. 

**Project Concept: AI-Driven Contextual Ad Relevance & Bidding Engine**
Media.net is a leader in contextual advertising. I want to build a backend system that simulates taking a webpage's context, using an LLM to quickly analyze it, and matching it against a database of ad campaigns to serve the most relevant ad in real-time.

Please provide a comprehensive project blueprint and the core code implementation. 

**Requirements:**
1. **Tech Stack:** Python (FastAPI) or Java (Spring Boot) - choose the one best for clean, production-quality code. 
2. **System Architecture:** 
   - A REST API endpoint that receives a webpage URL or text.
   - Integration with a caching layer (e.g., Redis) to store frequently analyzed page contexts for low-latency retrieval (simulating high-scale real-time requirements).
   - A relational database (e.g., PostgreSQL) schema for advertisers, ad campaigns, bids, and targeting categories.
3. **AI Integration:** 
   - Integrate with the OpenAI or Anthropic API to classify the webpage content into IAB (Interactive Advertising Bureau) categories and extract key topics.
   - Ensure the AI prompt is optimized for speed and structured JSON output.
4. **Core Ad-Tech Logic (The "Secret Sauce"):** 
   - Implement an algorithm that combines the AI-derived relevance score with advertiser bid prices to determine the winning ad (a simplified Real-Time Bidding auction).
5. **Engineering Best Practices:**
   - Object-Oriented Design (OOD) principles.
   - Clean code with strong type hinting and comprehensive error handling.
   - Include examples of Unit Tests (to demonstrate Test-Driven Development knowledge).
6. **Documentation & Trade-offs (Crucial for the interview):**
   - Provide a stellar `README.md`.
   - Include a section detailing the **"Engineering Trade-offs"** made in this design (e.g., consistency vs. availability, latency vs. AI accuracy, caching strategies).
   - Explain how this architecture scales to handle Media.net's volume of requests.

Start by giving me the system architecture diagram (in Mermaid.js format) and the database schema, followed by the core application code.

***
