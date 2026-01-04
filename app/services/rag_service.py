import chromadb
import uuid
from typing import List, Tuple, Dict
from app.repositories.resume_repository import ResumeRepository
from app.repositories.job_description_repository import JobDescriptionRepository
from app.models.resume_data import ResumeData
from app.models.job_description_data import JobDescriptionData

class RagService:
    def __init__(self):
        # Ephemeral client for now as requested
        self.client = chromadb.Client()
        self.resume_repository = ResumeRepository()
        self.jd_repository = JobDescriptionRepository()
    
    async def store_resume(self, resume_id: str) -> str:
        """
        Fetches a resume, processes it, and stores it in a dedicated ChromaDB collection.
        Returns the collection name.
        """
        resume = await self.resume_repository.get_resume_by_id(resume_id)
        if not resume:
            raise ValueError(f"Resume with ID {resume_id} not found")
            
        collection_name = f"resume_{resume_id}"
        
        # Cleanup existing collection if it exists (for idempotency in this ephemeral/test context)
        try:
            self.client.delete_collection(name=collection_name)
        except ValueError:
            pass # Collection didn't exist
            
        collection = self.client.create_collection(name=collection_name)
        
        documents, metadatas, ids = self._process_resume_for_chroma(resume.content.model_dump())
        
        if documents:
            collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
        return collection_name

    async def store_job_description(self, jd_id: str) -> str:
        """
        Fetches a job description, processes its structured data, and stores it in a dedicated ChromaDB collection.
        Returns the collection name.
        """
        jd = await self.jd_repository.get_job_description_by_id(jd_id)
        if not jd or not jd.structured_data:
            raise ValueError(f"Job Description with ID {jd_id} not found or missing structured data")

        collection_name = f"job_description_{jd_id}"
        
        try:
            self.client.delete_collection(name=collection_name)
        except ValueError:
            pass 
            
        collection = self.client.create_collection(name=collection_name)
        
        documents, metadatas, ids = self._process_jd_for_chroma(jd.structured_data.model_dump())
        
        if documents:
            collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
        return collection_name

    def _process_jd_for_chroma(self, jd_json: dict) -> Tuple[List[str], List[Dict], List[str]]:
        """
        Convert a JD JSON object into documents, metadatas and ids for ChromaDB.
        """
        documents: List[str] = []
        metadatas: List[Dict] = []
        ids: List[str] = []

        # Process Responsibilities
        for responsibility in jd_json.get("responsibilities", []):
            if not responsibility: continue
            documents.append(responsibility)
            metadatas.append({
                "type": "responsibility",
                "role": jd_json.get("role") or "Unknown Role",
                "company": jd_json.get("company") or "Unknown Company"
            })
            ids.append(str(uuid.uuid4()))

        # Process Requirements
        for requirement in jd_json.get("requirements", []):
            if not requirement: continue
            documents.append(requirement)
            metadatas.append({
                "type": "requirement",
                "role": jd_json.get("role") or "Unknown Role",
            })
            ids.append(str(uuid.uuid4()))

        # Process Summary
        if jd_json.get("summary"):
            documents.append(jd_json["summary"])
            metadatas.append({"type": "summary"})
            ids.append("jd_summary_01")

        # Process Tech Stack
        tech_stack = jd_json.get("tech_stack", [])
        if tech_stack:
            tech_summary = "Tech stack includes: " + ", ".join(tech_stack)
            documents.append(tech_summary)
            metadatas.append({"type": "tech_stack"})
            ids.append("jd_tech_stack_01")
            
        # Process Benefits
        for benefit in jd_json.get("benefits", []):
            if not benefit: continue
            documents.append(benefit)
            metadatas.append({"type": "benefit"})
            ids.append(str(uuid.uuid4()))

        return documents, metadatas, ids
        
    def _process_resume_for_chroma(self, resume_json: dict) -> Tuple[List[str], List[Dict], List[str]]:
        """
        Convert a resume JSON object into documents, metadatas and ids for ChromaDB.
        """
        documents: List[str] = []
        metadatas: List[Dict] = []
        ids: List[str] = []

        # Process Experience
        for job in resume_json.get("experience", []):
            # responsibilities might be a list or string depending on extraction
            responsibilities = job.get("description", []) # Mapped from ResumeData structure which uses 'description'
            
            # If it's a string, split lines. If list, use as is.
            if isinstance(responsibilities, str):
                responsibilities = [r.strip() for r in responsibilities.splitlines() if r.strip()]
            
            for responsibility in responsibilities:
                if not responsibility or not isinstance(responsibility, str):
                    continue
                documents.append(responsibility)
                metadatas.append({
                    "type": "experience",
                    "company": job.get("company") or "Unknown Company",
                    "position": job.get("role") or "Unknown Position", # 'role' in ResumeData
                    "startDate": job.get("date") or "Unknown", # 'date' in ResumeData
                    # ResumeData doesn't strictly have endDate separate, it uses 'date' string
                })
                ids.append(str(uuid.uuid4()))

        # Process Projects
        for project in resume_json.get("projects", []):
            name = project.get("name") or ""
            desc = project.get("description") or ""
            technologies = ", ".join(project.get("technologies", []))
            
            doc_content = f"{name}: {desc}. Technologies: {technologies}".strip()
            
            if not doc_content:
                continue
                
            documents.append(doc_content)
            metadatas.append({
                "type": "project",
                "name": name or "Unknown Project",
            })
            ids.append(str(uuid.uuid4()))

        # Process Skills
        skill_list = resume_json.get("skills", [])
        if skill_list:
            skill_summary = "Key technical skills include: " + ", ".join(skill_list)
            documents.append(skill_summary)
            metadatas.append({"type": "skills_summary"})
            ids.append("skills_summary_01")

        # Process Summary
        if resume_json.get("summary"):
            documents.append(resume_json["summary"])
            metadatas.append({"type": "summary"})
            ids.append("main_summary_01")

        # Process Education
        for education in resume_json.get("education", []):
            institution = education.get("institution") or ""
            degree = education.get("degree") or ""
            date = education.get("date") or ""
            
            doc_content = f"{degree} from {institution} ({date})".strip()
            if not doc_content:
                continue
                
            documents.append(doc_content)
            metadatas.append({
                "type": "education",
                "institution": institution,
                "degree": degree,
                "date": date
            })
            ids.append(str(uuid.uuid4()))

        return documents, metadatas, ids