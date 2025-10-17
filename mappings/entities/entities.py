from dataclasses import dataclass, field
from typing import List, Optional, Dict, Union

# 1. Polymer
@dataclass
class Polymer:
    id: str
    type: str = "Polymer"
    name: str = ""
    synonyms: List[str] = field(default_factory=list)
    CAS_number: Optional[str] = None
    polymer_class: Optional[str] = None
    density_range: Optional[Dict[str, Union[float, str]]] = None
    typical_additives: List[str] = field(default_factory=list)
    spectral_library_refs: List[str] = field(default_factory=list)
    external_refs: List[str] = field(default_factory=list)
    notes: Optional[str] = None

# 2. ParticleSizeClass
@dataclass
class ParticleSizeClass:
    id: str
    type: str = "ParticleSizeClass"
    label: str = ""
    min_micrometer: float = 0.0
    max_micrometer: float = 0.0
    bin_type: Optional[str] = None
    synonyms: List[str] = field(default_factory=list)
    definition_notes: Optional[str] = None

# 3. Shape
@dataclass
class Shape:
    id: str
    type: str = "Shape"
    label: str = ""
    synonyms: List[str] = field(default_factory=list)
    definition_notes: Optional[str] = None
    artifact_notes: Optional[str] = None

# 4. Source
@dataclass
class Source:
    id: str
    type: str = "Source"
    label: str = ""
    source_type: str = ""
    sector: Optional[str] = None
    emission_rate_estimate: Optional[Dict[str, Union[float, str]]] = None
    mitigation_options_ref: List[str] = field(default_factory=list)
    notes: Optional[str] = None

# 5. Method
@dataclass
class Method:
    id: str
    type: str = "Method"
    method_class: str = ""
    min_size_reliable: Optional[float] = None
    max_size_reliable: Optional[float] = None
    identification_capability: Optional[str] = None
    reporting_basis: Optional[str] = None
    LOD: Optional[float] = None
    LOQ: Optional[float] = None
    detects_particles: Optional[bool] = None
    identifies_polymer: Optional[bool] = None
    quantifies_mass: Optional[bool] = None
    sample_prep_requirements: Optional[str] = None
    known_biases: Optional[str] = None
    interlab_performance_notes: Optional[str] = None

# 6. EnvironmentalCompartment
@dataclass
class EnvironmentalCompartment:
    id: str
    type: str = "EnvironmentalCompartment"
    label: str = ""
    subcompartment: Optional[str] = None
    geo_context: Optional[Dict[str, str]] = None
    depth_or_height_range: Optional[Dict[str, Union[float, str]]] = None
    medium_properties: Optional[Dict[str, Union[float, str]]] = None
    notes: Optional[str] = None

# 7. Sample
@dataclass
class Sample:
    id: str
    type: str = "Sample"
    matrix: str = ""
    collection_date: str = ""
    location: Optional[Dict[str, Union[float, str]]] = None
    depth_or_height: Optional[float] = None
    volume_or_mass_processed: Optional[float] = None
    volume_or_mass_unit: Optional[str] = None
    sample_prep: Optional[str] = None
    contamination_controls: Optional[str] = None
    storage_conditions: Optional[str] = None
    collector: Optional[str] = None
    notes: Optional[str] = None

# 8. Observation
@dataclass
class Observation:
    id: str
    type: str = "Observation"
    sample_ref: str = ""
    method_ref: str = ""
    polymer_ref: Optional[str] = None
    size_class_ref: Optional[str] = None
    shape_ref: Optional[str] = None
    compartment_ref: Optional[str] = None
    value: float = 0.0
    unit: str = ""
    value_uncertainty: Optional[float] = None
    LOD: Optional[float] = None
    LOQ: Optional[float] = None
    replicate_n: Optional[int] = None
    spectral_match_confidence: Optional[float] = None
    calibration_ref: Optional[str] = None
    corrections_applied: List[str] = field(default_factory=list)
    QC_flags: List[str] = field(default_factory=list)
    citation_ref: Optional[str] = None
    measurement_date: Optional[str] = None

# 9. ExposurePathway
@dataclass
class ExposurePathway:
    id: str
    type: str = "ExposurePathway"
    pathway_label: str = ""
    route: str = ""
    intake_metric: Optional[str] = None
    population_context: Optional[str] = None
    assumptions_notes: Optional[str] = None
    citations_ref: List[str] = field(default_factory=list)

# 10. Mechanism
@dataclass
class Mechanism:
    id: str
    type: str = "Mechanism"
    label: str = ""
    evidence_type: Optional[str] = None
    dose_context: Optional[Dict[str, Union[float, str]]] = None
    key_biomarkers: List[str] = field(default_factory=list)
    species_scope: Optional[str] = None
    notes: Optional[str] = None
    citations_ref: List[str] = field(default_factory=list)

# 11. Biomarker
@dataclass
class Biomarker:
    id: str
    type: str = "Biomarker"
    name: str = ""
    assay_type: Optional[str] = None
    tissue_matrix: Optional[str] = None
    direction_of_change: Optional[str] = None
    threshold: Optional[float] = None
    threshold_unit: Optional[str] = None
    clinical_relevance_notes: Optional[str] = None
    citations_ref: List[str] = field(default_factory=list)

# 12. TissueOrgan
@dataclass
class TissueOrgan:
    id: str
    type: str = "TissueOrgan"
    label: str = ""
    species: Optional[str] = None
    histology_notes: Optional[str] = None
    vulnerability_notes: Optional[str] = None
    citations_ref: List[str] = field(default_factory=list)

# 13. ClinicalOutcome
@dataclass
class ClinicalOutcome:
    id: str
    type: str = "ClinicalOutcome"
    label: str = ""
    outcome_type: Optional[str] = None
    population: Optional[str] = None
    strength_of_evidence: Optional[str] = None
    citations_ref: List[str] = field(default_factory=list)
    notes: Optional[str] = None

# 14. PolicyInstrument
@dataclass
class PolicyInstrument:
    id: str
    type: str = "PolicyInstrument"
    title: str = ""
    jurisdiction: str = ""
    effective_dates: Optional[Dict[str, Optional[str]]] = None
    scope: Optional[str] = None
    targeted_sources: List[str] = field(default_factory=list)
    required_metrics: List[str] = field(default_factory=list)
    compliance_requirements: Optional[str] = None
    notes: Optional[str] = None
