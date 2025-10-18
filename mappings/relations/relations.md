# Relationship types (edge properties kept lean)

## Microplastics Ontology: Key Relationships

- **Sample**  
  - *collected_from* → EnvironmentalCompartment  
  - *processed_by* → Method  
  - *produces* → Observation  

- **Observation**  
  - *about_sample* → Sample  
  - *identified_by* → Method  
  - *has_size_class* → ParticleSizeClass  
  - *has_shape* → Shape  
  - *has_polymer* → Polymer  
  - *located_in* → EnvironmentalCompartment  
  - *has_value* (count/mass/unit)  

- **ParticleSizeClass**  
  - *used_in* → Observation  

- **Shape**  
  - *used_in* → Observation  

- **Polymer**  
  - *used_in* → Observation  
  - *source_of* → Source  

- **Source**  
  - *emits_to* → EnvironmentalCompartment  
  - *releases* → Sample/Observation (linked via compartment/sample/event)  

- **Method**  
  - *detects* → Polymer, Shape, SizeClass  
  - *used_for* → Sample/Observation  

- **EnvironmentalCompartment**  
  - *contains* → Sample, Observation, Source  
  - *affected_by* → Source, PolicyInstrument  

- **ExposurePathway**  
  - *links* → EnvironmentalCompartment → TissueOrgan  
  - *context_for* → Mechanism, Biomarker, ClinicalOutcome  

- **Mechanism**  
  - *evidenced_by* → Biomarker  
  - *impacts* → TissueOrgan  

- **Biomarker**  
  - *measured_in* → TissueOrgan  
  - *influences* → ClinicalOutcome  

- **TissueOrgan**  
  - *shows_effect* → Biomarker, Mechanism  
  - *result_of* → ExposurePathway  

- **ClinicalOutcome**  
  - *arises_from* → Mechanism, TissueOrgan  
  - *studied_via* → ExposurePathway  

- **PolicyInstrument**  
  - *targets* → Source, EnvironmentalCompartment, Polymer  
  - *requires* → Method, Observation, Reporting Metric

---

## Typical Example Pathways

- `Source` → *emits_to* → `EnvironmentalCompartment` → *sampled_by* → `Sample` → *analyzed_by* → `Method` → *generates* → `Observation` → *has_shape*, *has_size_class*, *has_polymer*
- `EnvironmentalCompartment` → *exposes* → `ExposurePathway` → *acts_on* → `TissueOrgan` → *marked_by* → `Biomarker` → *results_in* → `ClinicalOutcome`
- `PolicyInstrument` → *regulates* → `Source`/`Compartment`/`Method`, *requires* reporting of `Observation` with specified `metrics`

