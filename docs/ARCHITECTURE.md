# Inspector IA: Technical Documentation

## Executive Overview

Inspector IA represents a comprehensive forensic intelligence platform designed to support investigative journalism through advanced pattern detection in public financial data. The system employs graph analysis, machine learning, and explainable artificial intelligence to identify anomalous patterns in public figures' financial activities while maintaining strict ethical guidelines and human oversight requirements.

The platform operates on a fundamental principle: it generates risk alerts based on public data analysis, requiring mandatory verification by professional journalists before any publication. The system identifies statistical anomalies and suspicious patterns, not criminal activity, serving as an investigative tool rather than a judicial mechanism.

## System Architecture

The Inspector IA platform implements a microservices architecture built on modern cloud-native principles. The system comprises five primary layers that work in concert to process data, detect patterns, and present findings to investigative journalists.

The presentation layer consists of a React-based journalist dashboard that provides intuitive access to risk assessments, network visualizations, and temporal analysis. This interface connects to the API gateway layer, implemented in FastAPI, which orchestrates communication between frontend clients and backend microservices.

The core processing layer contains four specialized microservices. The data ingestion microservice handles collection, normalization, and validation of information from diverse sources including open-source intelligence, corporate registries, and financial disclosures. The graph analysis microservice performs network analysis using Neo4j to identify complex relationships and suspicious connection patterns. The anomaly detection microservice applies machine learning algorithms to identify statistical deviations and known fraud patterns. The explainable AI microservice generates human-readable explanations for every alert, ensuring journalists understand the reasoning behind risk assessments.

The data persistence layer employs a polyglot approach optimized for different data types. PostgreSQL serves as the primary data lake for structured information. Neo4j maintains the knowledge graph representing relationships between entities. Pinecone stores vector embeddings for semantic search capabilities. A blockchain layer provides immutable audit trails for data provenance verification.

Communication between microservices occurs through a message bus implemented with RabbitMQ or Kafka, enabling asynchronous processing and system resilience. This architecture ensures scalability, fault tolerance, and maintainability while supporting the complex analytical requirements of investigative journalism.

## Anomaly Risk Index (IRA)

The Anomaly Risk Index serves as the core quantitative measure of suspicious activity within the Inspector IA system. The index employs a weighted multi-dimensional formula that evaluates three primary aspects of potential fraudulent behavior.

The mathematical representation takes the form: IRA equals the sum of three weighted scores plus a network complexity bonus. The patrimonial dimension receives a weight of thirty percent and examines unexplained wealth accumulation, asset-income discrepancies, and sudden changes in declared assets. The network dimension carries the highest weight at forty percent, analyzing connection patterns to offshore entities, shell companies, and individuals with suspicious financial histories. The temporal dimension contributes thirty percent, identifying suspicious timing correlations between legislative actions and financial movements, or coincidences between travel patterns and monetary transactions.

The network complexity bonus can contribute up to thirty additional points based on the sophistication of obfuscation techniques detected. This bonus increases with the number of intermediary layers, geographic jurisdiction diversity, and use of advanced concealment methods such as cryptocurrency mixers or privacy-focused digital assets.

The resulting score maps to five risk categories that guide journalistic action. Scores from zero to twenty indicate cosmic background noise requiring only routine monitoring. Values between twenty-one and fifty suggest nebular suspicion warranting deeper analysis. Scores of fifty-one to seventy represent stellar anomalies that merit priority investigation. Results from seventy-one to eighty-five trigger supernova alerts for publication consideration. Scores exceeding eighty-five indicate black hole critical situations demanding urgent investigation.

This scoring system provides journalists with quantitative guidance while maintaining the requirement for human judgment in all investigative decisions.

## Fraud Pattern Detection System

Inspector IA implements a comprehensive taxonomy of five major fraud patterns, each with specialized detection algorithms and unique risk signatures. These patterns represent the most common methods employed to conceal illicit financial activities in public sector contexts.

The CRYPTO_HIDING pattern addresses the use of cryptocurrency to obscure fund flows. This pattern implements three sophistication levels to train detection algorithms against increasingly complex evasion techniques. The basic level involves direct peer-to-peer transfers through exchange-linked wallets with minimal obfuscation. The intermediate level incorporates decentralized exchange routing, multi-layer wallet structures, and initial mixing techniques. The advanced level deploys cascading mixer services, privacy-focused cryptocurrencies, cross-chain bridge transactions, and temporal obfuscation strategies. Detection focuses on identifying mixer interactions, privacy coin conversions, structured transaction amounts designed to avoid reporting thresholds, peeling chain patterns where large transfers fragment into numerous smaller transactions, and complex multi-layer wallet architectures.

The OFFSHORE_LAUNDERING pattern targets the use of foreign jurisdictions and shell company networks to disguise asset ownership. Detection mechanisms analyze nominee shareholder arrangements, circular ownership structures, jurisdiction hopping patterns, and beneficial ownership concealment through corporate layers. The system correlates these structures with unexplained wealth and suspicious transaction timing.

The TRAVEL_COINCIDENCE pattern employs temporal-spatial correlation analysis to identify suspicious alignments between physical presence in tax havens or specific jurisdictions and subsequent financial movements. This pattern integrates flight manifests, diplomatic calendars, and financial transaction data to detect non-coincidental timing relationships.

The GHOST_COMPANY pattern identifies entities that exist primarily to facilitate corruption rather than conduct legitimate business operations. These companies typically exhibit minimal operational activity, lack substantive business premises or staff, yet receive substantial government contracts or serve as intermediaries in high-value transactions. Detection algorithms analyze business registry data, tax filings, employment records, and procurement databases to identify these suspicious entities.

The INSIDER_TRADING pattern focuses on public officials who exploit non-public information for financial gain. Detection examines correlations between voting records, committee assignments, pending legislation, and personal or family asset acquisitions. The system identifies patterns of asset accumulation that precede public announcements or policy changes that subsequently increase asset values.

Each pattern contributes specific risk score components to the overall IRA calculation, with bonuses ranging from five to thirty points depending on sophistication level and evidence strength.

## Synthetic Fraud Ecosystem

The Synthetic Fraud Ecosystem represents a critical component for training and validating detection algorithms without requiring real-world fraudulent data. This system generates realistic synthetic cases that mirror the complexity and characteristics of actual corruption patterns while maintaining complete control over ground truth labels.

The ecosystem operates through a sophisticated multi-stage generation pipeline. The base politician generator creates realistic profiles including income levels, asset declarations, family connections, political positions, and voting histories. These profiles follow statistical distributions observed in real public official data, ensuring synthetic cases exhibit realistic variance and characteristics.

The pattern injection engine then overlays fraud patterns onto a subset of these clean profiles. For each pattern type, the engine configures parameters including severity level, sophistication degree, temporal characteristics, and network complexity. The injection process creates complete transaction histories, network connections, and temporal sequences that implement the specified fraud pattern while maintaining internal consistency and realism.

The CRYPTO_HIDING injector demonstrates the sophistication of this approach through its three-level implementation. For basic level patterns, the injector creates simple wallet structures with direct transfers and minimal intermediaries. The intermediate level constructs two-layer wallet architectures incorporating decentralized exchanges and initial mixing techniques. The advanced level generates complex three-layer structures with privacy coin conversions, cross-chain transactions, and sophisticated obfuscation timing.

Each injected pattern includes comprehensive ground truth metadata. This metadata specifies all techniques employed, exact transaction amounts and timing, complete network topology, and expected detection signals. The system generates validation datasets where detection algorithms must distinguish between clean profiles and profiles with injected fraud patterns across varying sophistication levels.

The synthetic ecosystem enables rigorous algorithm testing without privacy concerns or legal complications. It allows systematic evaluation of detection sensitivity, false positive rates, and robustness against evasion techniques. The ecosystem can generate datasets at scale, producing thousands of realistic cases for machine learning training and validation.

Statistical validators ensure synthetic data maintains realistic characteristics by comparing distributions against known patterns in public data. Realism validators assess whether generated cases would appear plausible to domain experts. Ground truth validators verify that all injected patterns contain complete and accurate metadata for subsequent evaluation.

## Implementation Technology Stack

Inspector IA employs a carefully selected technology stack optimized for the unique requirements of forensic data analysis and investigative journalism support.

The core backend implementation uses Python 3.10 or later for its extensive data science libraries and rapid development capabilities. Performance-critical components incorporate Rust implementations where execution speed becomes paramount. Database interactions employ ANSI SQL 2016 standards for maximum portability and compatibility.

The data persistence layer implements a polyglot database strategy. Neo4j version 5.0 or Amazon Neptune serve as the primary graph database, enabling efficient traversal of complex relationship networks. PostgreSQL 15 or later, enhanced with TimescaleDB extensions, provides relational data storage with time-series optimization. Pinecone or Weaviate host vector embeddings for semantic search capabilities. Redis 7.0 or later implements caching layers for frequent access patterns.

Data processing frameworks operate at multiple scales. Apache Spark 3.4 or later handles batch processing for historical analysis and model training. Apache Flink 1.17 or later enables stream processing for near-real-time detection. Apache Airflow 2.7 or later orchestrates complex data pipelines and scheduling.

The machine learning ecosystem builds on PyTorch 2.0 and TensorFlow 2.13 or later as primary frameworks. PyTorch Geometric and Deep Graph Library provide specialized graph neural network capabilities. SpaCy 3.6 and Hugging Face Transformers enable natural language processing for document analysis. SHAP, LIME, and Captum implement explainable AI requirements. PyOD, Isolation Forest implementations, and custom autoencoders provide anomaly detection algorithms.

The frontend dashboard implements Next.js 14 or later with TypeScript for type safety and development efficiency. D3.js 7.0 and Cytoscape.js 3.25 or later render interactive visualizations. Tailwind CSS 3.3 and ShadCN UI components provide consistent styling. Zustand and React Query manage state and server communication.

Infrastructure automation leverages Docker and Docker Compose for containerization. Kubernetes, specifically k3s for development environments, orchestrates container deployment and scaling. GitHub Actions implements continuous integration and deployment pipelines. Terraform and Pulumi define infrastructure as code. Prometheus, Grafana, and Loki provide comprehensive monitoring and observability. HashiCorp Vault manages secrets and sensitive configuration.

This technology stack balances cutting-edge capabilities with production stability, ensuring the system can handle complex analytical workloads while maintaining security and reliability standards appropriate for sensitive investigative work.

## Security and Ethical Framework

Inspector IA implements defense-in-depth security measures reflecting the sensitive nature of investigative journalism and the potential consequences of data breaches or misuse.

Data encryption employs AES-256-GCM for information at rest, protecting stored data from unauthorized access. Transport layer security uses TLS 1.3 for all network communications. Authentication implements OAuth 2.1 with short-lived JWT tokens, minimizing exposure windows for compromised credentials. Authorization follows role-based access control enhanced with attribute-based policies, ensuring users access only information necessary for their specific investigations.

Every system action generates immutable audit trail entries, with cryptographic anchoring to blockchain infrastructure preventing tampering with historical records. This ensures complete accountability for all data access and analysis operations. Differential privacy techniques protect aggregate statistics, preventing the ability to infer individual-level information from summary data. GDPR and CCPA compliance mechanisms include automated anonymization pipelines and data deletion workflows.

The ethical framework establishes five fundamental principles that govern all system operations. Transparency First requires that all algorithms remain open to audit, with documentation explaining detection logic and scoring methodologies. Human-in-the-Loop mandates that no fully automated decisions occur, requiring journalist review before any investigative action. Privacy by Design implements data minimization and anonymization as default behaviors rather than optional enhancements. Accountability establishes clear responsibility chains for every system output and investigative action. Beneficial Use restricts system employment exclusively to legitimate investigative journalism serving the public interest.

The platform maintains absolute prohibitions against specific use cases. Mass surveillance of private citizens remains strictly forbidden regardless of claimed justification. Discrimination based on protected characteristics cannot occur within detection algorithms or investigative workflows. Automated publication without human review violates core principles regardless of confidence levels. Sale of data to third parties stands prohibited under all circumstances. Political targeting or manipulation for partisan purposes represents a fundamental misuse that voids all usage permissions.

These security measures and ethical constraints protect both the subjects of investigation and the journalists employing the system, ensuring Inspector IA serves its intended purpose without enabling abuse or overreach.

## Development Workflow and Contributing

Organizations and individuals interested in contributing to Inspector IA should follow established development patterns that maintain code quality and system integrity while enabling collaborative improvement.

The development environment setup begins with cloning the repository from the mechmind-dwv organization on GitHub. Dependency installation follows standard Python practices using pip and the provided requirements file. Environment configuration employs a template file that developers customize with appropriate credentials and settings for their development infrastructure.

The codebase follows strict naming conventions that enhance readability and maintainability. Python modules employ snake_case naming. React components use PascalCase. Configuration files adopt kebab-case formatting. These conventions eliminate ambiguity and enable developers to quickly locate relevant code.

Git workflow implements a structured branching strategy. The main branch contains production-ready code with rigorous quality gates. The develop branch hosts active development work undergoing integration testing. Feature branches implement new capabilities, following the naming pattern feature/descriptive-name. Fix branches address identified defects using fix/problem-description format. Release branches prepare specific versions for deployment as release/version-number.

Commit messages follow conventional commit standards with emoji prefixes for visual scanning. Feature additions use the sparkles emoji and feat scope. Bug corrections employ the wrench emoji and fix scope. Documentation updates prefix with the books emoji and docs scope. Test additions leverage the test tube emoji and test scope. This convention enables automated changelog generation and commit categorization.

Pull requests require comprehensive content before acceptance. All new functionality must include automated tests demonstrating correct behavior. Documentation updates must accompany code changes, ensuring the knowledge base remains current. Ethical impact assessments evaluate whether proposed changes align with platform principles and usage restrictions.

Contributors should focus initial efforts on areas marked as good first issues, which provide well-scoped introduction points. Documentation improvements offer valuable contributions that enhance system accessibility. Test coverage expansion strengthens confidence in system behavior. Example investigation scenarios help validate real-world applicability of detection algorithms.

The platform welcomes diverse contributor profiles. Investigative journalists validate use cases, provide workflow feedback, and test dashboard usability. AI and machine learning researchers develop novel detection algorithms, improve explainable AI outputs, and optimize graph neural networks. Software engineers build scalable data pipelines, implement real-time graph analysis, and develop secure auditable systems. Legal and ethics experts navigate international data protection laws, develop usage guidelines, and create journalist protection protocols.

This collaborative development model ensures Inspector IA evolves to meet the practical needs of investigative journalism while maintaining technical excellence and ethical integrity.

## Deployment and Operations

Inspector IA deployment follows cloud-native principles enabling operation across diverse infrastructure environments from development laptops to production cloud platforms.

The development environment leverages Docker Compose to orchestrate local instances of all required services. This configuration includes PostgreSQL for structured data, Neo4j for graph storage, Redis for caching, and RabbitMQ for message passing. Developers can initialize a complete functional environment with a single command, enabling rapid iteration and testing.

Production deployment employs Kubernetes for container orchestration, providing horizontal scaling, health monitoring, and automated recovery. The infrastructure definition uses Terraform and Pulumi, capturing cluster configuration as version-controlled code. This approach enables reproducible deployments across multiple environments and cloud providers.

The monitoring infrastructure implements comprehensive observability through Prometheus for metrics collection, Grafana for visualization and alerting, and Loki for log aggregation. Custom dashboards track system health indicators including API response times, graph query performance, machine learning inference latency, and data ingestion throughput. Alert rules notify operations personnel of anomalous conditions requiring intervention.

Deployment follows a phased approach aligned with system maturity. The current phase focuses on architecture finalization and synthetic data generation. The second phase implements core detection engines and data ingestion pipelines for pilot countries. The third phase launches journalist beta programs with media partners and expands geographic coverage. The fourth phase scales to global operation with real-time monitoring capabilities and collaborative investigation features.

This operational model balances accessibility for development and testing with robustness and security for production investigative work.

## Conclusion and Future Direction

Inspector IA represents a significant advancement in the application of artificial intelligence to investigative journalism. By combining graph analysis, machine learning, and explainable AI within a rigorous ethical framework, the platform enables journalists to identify suspicious financial patterns that would remain hidden in traditional manual analysis.

The system's architecture prioritizes transparency, human oversight, and data integrity while delivering sophisticated analytical capabilities. The synthetic fraud ecosystem enables robust algorithm training without compromising privacy or requiring access to sensitive real-world fraud data. The multi-dimensional risk scoring system provides quantitative guidance while preserving essential human judgment in investigative decisions.

Future development will expand detection capabilities to additional fraud patterns, increase geographic coverage, and enhance real-time monitoring functionality. The platform aims to become the standard tool for financial investigative journalism worldwide, supporting accountability and transparency in public sector financial activities while respecting privacy rights and maintaining strict ethical standards.

The success of Inspector IA ultimately depends on the investigative journalists who employ it, transforming algorithmic insights into verified public interest reporting. The platform serves as a force multiplier for human judgment and journalistic integrity rather than a replacement for either.
