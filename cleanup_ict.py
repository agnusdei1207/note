import os
import shutil

base_dir = 'content/studynote/06_ict_convergence'

moves = [
    ('uncategorized/255_apache_airflow_dag.md', '03_cloud_infrastructure'),
    ('uncategorized/256_apache_kafka_pub_sub.md', '03_cloud_infrastructure'),
    ('uncategorized/257_observability_opentelemetry.md', '03_cloud_infrastructure'),
    ('uncategorized/258_low_code_no_code.md', '03_cloud_infrastructure'),
    ('uncategorized/259_citizen_developer.md', '03_cloud_infrastructure'),
    ('uncategorized/260_sdv_software_defined_vehicle.md', '02_iot_mobility'),
    ('uncategorized/283_lora_low_rank_adaptation.md', '04_ai_llm'),
    ('uncategorized/284_quantization_qlora_model_compression.md', '04_ai_llm'),
    ('uncategorized/285_knowledge_distillation.md', '04_ai_llm'),
    ('uncategorized/286_multimodal_ai.md', '04_ai_llm'),
    ('uncategorized/287_diffusion_model.md', '04_ai_llm'),
    ('uncategorized/288_latent_diffusion_model.md', '04_ai_llm'),
    ('uncategorized/289_diffusion_vs_gan.md', '04_ai_llm'),
    ('uncategorized/290_autoregressive_generation.md', '04_ai_llm'),
    ('uncategorized/291_kv_cache.md', '04_ai_llm'),
    ('uncategorized/292_pagedattention_vllm.md', '04_ai_llm'),
    ('uncategorized/293_ai_agents.md', '04_ai_llm'),
    ('uncategorized/294_function_calling_tool_use.md', '04_ai_llm'),
    ('uncategorized/295_moe_mixture_of_experts.md', '04_ai_llm'),
    ('uncategorized/296_mlops_machine_learning_operations.md', '04_ai_llm'),
    ('uncategorized/297_llmops_pipeline.md', '04_ai_llm'),
    ('uncategorized/298_model_drift_data_drift.md', '04_ai_llm'),
    ('uncategorized/299_feature_store.md', '04_ai_llm'),
    ('uncategorized/301_ai_safety_red_teaming.md', '04_ai_llm'),
    ('uncategorized/302_prompt_injection_jailbreak.md', '04_ai_llm'),
    ('uncategorized/303_xai_explainable_ai.md', '04_ai_llm'),
    ('uncategorized/304_lime_shap_contributions.md', '04_ai_llm'),
    # 300 is duplicate, handled later
    ('04_ai_llm/399_manifold_hypothesis_dimensionality_reduction.md', '05_data_science'),
    ('04_ai_llm/422_a_star_admissible_heuristic.md', '05_data_science'),
    ('04_ai_llm/377_perceptron_convergence_theorem.md', '05_data_science'),
    ('04_ai_llm/415_rag_rerank_cross_encoder.md', '05_data_science'),
    ('04_ai_llm/380_computational_graph_lazy_eager_execution.md', '05_data_science'),
    ('04_ai_llm/413_clip_multimodal_contrastive_loss.md', '05_data_science'),
    ('04_ai_llm/361_vanishing_gradient_initialization.md', '05_data_science'),
    ('04_ai_llm/421_turing_test_machine_intelligence.md', '05_data_science'),
    ('04_ai_llm/409_model_quantization_error_penalty.md', '05_data_science'),
    ('04_ai_llm/382_fuzzy_logic_min_max_membership.md', '05_data_science'),
    ('04_ai_llm/423_mcts_monte_carlo_tree_search.md', '05_data_science'),
    ('04_ai_llm/410_ai_intellectual_property_data_sovereignty_data_act.md', '05_data_science'),
    ('04_ai_llm/412_tcn_dilated_causal_convolution.md', '05_data_science'),
    ('04_ai_llm/411_ontology_knowledge_representation_owl_rdf.md', '05_data_science'),
    ('04_ai_llm/381_autograd_chain_rule.md', '05_data_science'),
    ('04_ai_llm/414_llm_decoder_top_k_temperature.md', '05_data_science'),
    ('04_ai_llm/416_prompt_injection_semantic_routing.md', '05_data_science'),
    ('05_data_science/468_model_drift_retraining.md', '04_ai_llm'),
    ('05_data_science/467_feature_store_data_sharing.md', '04_ai_llm'),
    ('05_data_science/466_mlops_pipeline_ci_cd_ct.md', '04_ai_llm'),
]

for src_rel, dst_folder in moves:
    src = os.path.join(base_dir, src_rel)
    dst = os.path.join(base_dir, dst_folder, os.path.basename(src_rel))
    if os.path.exists(src):
        print(f"Moving {src} to {dst}")
        shutil.move(src, dst)

# Delete corrupted files in 04_ai_llm (261-282)
for i in range(261, 283):
    # Find file with prefix i
    folder_path = os.path.join(base_dir, '04_ai_llm')
    for filename in os.listdir(folder_path):
        if filename.startswith(f"{i}_") or filename.startswith(f"{i:03d}_"):
            file_path = os.path.join(folder_path, filename)
            print(f"Deleting corrupted file: {file_path}")
            os.remove(file_path)

# Resolve duplicates
# 98: 098_the_graph_indexing_protocol_web3.md seems more descriptive?
# Actually list says "98. 블록체인 데이터 인덱싱 프로토콜 (The Graph)"
# I'll keep 098_the_graph_blockchain_indexing.md and delete the other.
p1 = os.path.join(base_dir, '01_blockchain/098_the_graph_indexing_protocol_web3.md')
if os.path.exists(p1):
    os.remove(p1)

# 300: duplicate in uncategorized and 04_ai_llm. Keep 04_ai_llm.
p2 = os.path.join(base_dir, 'uncategorized/300_vector_indexing_ann.md')
if os.path.exists(p2):
    os.remove(p2)

# 118: UWB in 02_iot_mobility is misnumbered.
p3 = os.path.join(base_dir, '02_iot_mobility/118_uwb_ultra_wideband.md')
if os.path.exists(p3):
    os.remove(p3)

print("Cleanup done.")
