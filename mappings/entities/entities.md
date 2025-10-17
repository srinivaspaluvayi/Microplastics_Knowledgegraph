# Node types and attributes

| Ontology Entity Group              | Matching Node Schemas                               |
|------------------------------------|-----------------------------------------------------|
| **Polymers**                       | Polymer                                             |
| **Size Classes**                   | ParticleSizeClass, Shape                            |
| **Sources**                        | Source                                              |
| **Detection Techniques**           | Method                                              |
| **Environmental Compartments**     | EnvironmentalCompartment                            |
| **Health Effects**                 | ExposurePathway, Mechanism, Biomarker, TissueOrgan, ClinicalOutcome |
| **Policy Context**                 | PolicyInstrument                                    |
| **Data/Linking Entities**          | Sample, Observation                                 |


## Polymer
- Purpose: Represent polymer materials detected/assessed.
- Key attributes: name (preferred label), synonyms, CAS_number, polymer_class (e.g., polyolefin, polyester), density_range (min,max,unit), typical_additives (list), spectral_library_refs (list), external_refs (CHEBI/CAS/other IDs), notes, version.

## ParticleSizeClass
- Purpose: Standardize size bins for comparability and reasoning.
- Key attributes: label, min_micrometer, max_micrometer, bin_type (nano/micro), synonyms, definition_notes, version.

## Shape
- Purpose: Standardize particle morphology categories.
- Key attributes: label (fiber, fragment, bead, film, foam), synonyms, definition_notes, artifact_notes, version.

## EnvironmentalCompartment
- Purpose: Where particles exist or are sampled.
- Key attributes: label (air, drinking water, marine water, sediment, soil, biota, human_tissue), subcompartment (e.g., surface, subsurface, microlayer), geo_context (region/country), depth_or_height_range, medium_properties (salinity, temperature, optional), notes, version.

## Source
- Purpose: Activities or products emitting microplastics.
- Key attributes: label (textiles, tire_wear, pellets, personal_care), source_type (primary/secondary), sector (e.g., transport, consumer), emission_rate_estimate (value, unit, context, optional), mitigation_options_ref, notes, version.

## Sample
- Purpose: A specific collected specimen to be analyzed.
- Key attributes: sample_id, matrix (link to EnvironmentalCompartment), collection_date, location (lat, lon, region), depth_or_height, volume_or_mass_processed, sample_prep (digestion, filter type/size), contamination_controls (field/lab blanks), storage_conditions, collector, notes, version.

## Method
- Purpose: Analytical approach used for detection/quantification.
- Key attributes: method_class (µ-FTIR, µ-Raman, Py-GC/MS, TED-GC/MS, LDIR/QCL‑IR, NIR/HSI, etc.), min_size_reliable, max_size_reliable, identification_capability (polymer, shape, none), reporting_basis (count, mass, both), LOD, LOQ, detects_particles (bool), identifies_polymer (bool), quantifies_mass (bool), sample_prep_requirements, known_biases, interlab_performance_notes, citations_ref, version.

## Observation
- Purpose: A measured result connecting a sample, method, and particle characteristics.
- Key attributes: observation_id, sample_ref, method_ref, polymer_ref, size_class_ref, shape_ref, value, unit (count_per_volume | count_per_mass | mass_per_volume | mass_per_mass), value_uncertainty (± or CI), LOD, LOQ, replicate_n, spectral_match_confidence (if applicable), calibration_ref, corrections_applied (blank_subtraction, recovery_factor), QC_flags, citation_ref, measurement_date, evidence_weight (derived), version.

## ExposurePathway
- Purpose: Route linking environmental presence to human/biota exposure.
- Key attributes: pathway_label (e.g., ingestion_drinking_water, inhalation_indoor_air), route (oral, inhalation, dermal), intake_metric (name, unit), population_context (e.g., adults, infants, occupational), assumptions_notes, citations_ref, version.

## Mechanism
- Purpose: Biological mechanism of effect.
- Key attributes: label (oxidative_stress, inflammation, endocrine_disruption, genotoxicity), evidence_type (in_vitro, in_vivo, human_observational), dose_context (range, unit), key_biomarkers (list), species_scope, notes, citations_ref, version.

## Biomarker
- Purpose: Measurable indicator tied to a mechanism or outcome.
- Key attributes: name, assay_type, tissue_matrix, direction_of_change (increase/decrease), threshold (if known), clinical_relevance_notes, citations_ref, version.

## TissueOrgan
- Purpose: Target tissue/organ where effects occur or are measured.
- Key attributes: label (lung, gut, placenta, liver, kidney), species, histology_notes, vulnerability_notes, citations_ref, version.

## ClinicalOutcome
- Purpose: Health outcomes linked to exposure/mechanisms.
- Key attributes: label (respiratory_symptoms, cardiovascular_effects, reproductive_outcomes), outcome_type (symptom, diagnosis, function_metric), population (general, occupational, animal model), strength_of_evidence (qualitative scale), citations_ref, version.

## PolicyInstrument
- Purpose: Policy or regulation affecting sources/measurements.
- Key attributes: title, jurisdiction, effective_dates (start, end/ongoing), scope (primary MPs, secondary MPs, intentionally added, sectors), targeted_sources (list), required_metrics (count, mass, size ranges), compliance_requirements, version, notes.



