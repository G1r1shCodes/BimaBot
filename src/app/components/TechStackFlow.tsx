import { motion } from 'motion/react';
import { useEffect, useState } from 'react';
import bedrockImg from '/images/amazon bedrock.png';
import novaImg from '/images/Nova aws.png';
import titanEmbeddingImg from '/images/Amazon Titan Embedding v2.png';
import textractImg from '/images/Amazon Textract.png';
import s3Img from '/images/Amazon S3.png';

interface TechStackFlowProps {
  currentStep?: number;
  showcaseMode?: boolean;
}

const technologies = [
  {
    name: 'Amazon Bedrock',
    description: 'Foundation model access',
    icon: bedrockImg,
    color: 'from-blue-500 to-blue-600',
    active: 0
  },
  {
    name: 'Amazon Nova',
    description: 'Advanced AI analysis',
    icon: novaImg,
    color: 'from-purple-500 to-purple-600',
    active: 1
  },
  {
    name: 'Amazon Titan Embedding',
    description: 'Text embeddings',
    icon: titanEmbeddingImg,
    color: 'from-teal-500 to-teal-600',
    active: 1
  },
  {
    name: 'Amazon Textract',
    description: 'Document extraction',
    icon: textractImg,
    color: 'from-orange-500 to-orange-600',
    active: 2
  },
  {
    name: 'Amazon S3',
    description: 'Document storage',
    icon: s3Img,
    color: 'from-green-500 to-green-600',
    active: 2
  }
];

export default function TechStackFlow({ currentStep = 0, showcaseMode = false }: TechStackFlowProps) {
  const [activeNodes, setActiveNodes] = useState<number[]>([]);

  useEffect(() => {
    if (!showcaseMode) {
      // In processing mode, activate based on current step
      const activeIndices = technologies
        .map((tech, index) => (tech.active <= currentStep ? index : -1))
        .filter(index => index !== -1);

      setActiveNodes(activeIndices);
    }
  }, [currentStep, showcaseMode]);

  // Marquee mode for showcase
  if (showcaseMode) {
    // Duplicate technologies for seamless loop
    const duplicatedTechs = [...technologies, ...technologies];

    return (
      <div className="overflow-hidden py-8">
        <div className="text-center mb-8">
          <p className="text-sm text-gray-600">Powered by</p>
        </div>

        {/* Marquee Container */}
        <div className="relative">
          {/* Gradient overlays for fade effect */}
          <div className="absolute left-0 top-0 bottom-0 w-32 bg-gradient-to-r from-white to-transparent z-10 pointer-events-none" />
          <div className="absolute right-0 top-0 bottom-0 w-32 bg-gradient-to-l from-white to-transparent z-10 pointer-events-none" />

          {/* Scrolling marquee */}
          <motion.div
            className="flex gap-6"
            animate={{
              x: [0, -1 * (technologies.length * 280)]
            }}
            transition={{
              x: {
                duration: 30,
                repeat: Infinity,
                ease: "linear"
              }
            }}
          >
            {duplicatedTechs.map((tech, index) => (
              <motion.div
                key={`${tech.name}-${index}`}
                className="flex-shrink-0 w-64"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <div className="relative p-6 h-full">
                  {/* Shimmer effect */}
                  <motion.div
                    className="absolute inset-0 bg-gradient-to-r from-transparent via-gray-100 to-transparent opacity-30"
                    animate={{
                      x: ['-100%', '100%']
                    }}
                    transition={{
                      duration: 2,
                      repeat: Infinity,
                      ease: "easeInOut",
                      delay: index * 0.3
                    }}
                  />

                  <div className="relative z-10">
                    <div className="flex flex-col items-center gap-4 mb-3">
                      <img
                        src={tech.icon}
                        alt={tech.name}
                        className="w-16 h-16 object-contain"
                      />
                      <div className="text-center">
                        <div className="font-semibold text-gray-900 text-base leading-tight mb-1">
                          {tech.name}
                        </div>
                        <div className="text-sm text-gray-600">
                          {tech.description}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </div>
    );
  }

  // Grid mode for processing page
  return (
    <div className="mt-8 pt-8 border-t border-gray-200">
      <div className="text-center mb-6">
        <p className="text-sm text-gray-600">Powered by</p>
      </div>

      {/* Technology Grid with Animated Flow */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {technologies.map((tech, index) => {
          const isActive = activeNodes.includes(index);

          return (
            <motion.div
              key={tech.name}
              initial={{ opacity: 0, y: 20 }}
              animate={{
                opacity: isActive ? 1 : 0.4,
                y: 0,
                scale: isActive ? 1.05 : 1
              }}
              transition={{
                duration: 0.5,
                delay: index * 0.1,
                scale: {
                  duration: 0.3,
                  repeat: isActive ? Infinity : 0,
                  repeatType: "reverse",
                  repeatDelay: 1
                }
              }}
              className="relative"
            >
              <div
                className={`
                  relative overflow-hidden rounded-lg p-4 border-2 transition-all
                  ${isActive
                    ? 'border-teal-300 bg-white shadow-md'
                    : 'border-gray-200 bg-gray-50'
                  }
                `}
              >
                {/* Animated gradient background when active */}
                {isActive && (
                  <motion.div
                    className={`absolute inset-0 bg-gradient-to-br ${tech.color} opacity-5`}
                    animate={{
                      opacity: [0.05, 0.1, 0.05]
                    }}
                    transition={{
                      duration: 2,
                      repeat: Infinity,
                      ease: "easeInOut"
                    }}
                  />
                )}

                {/* Pulse effect for active technologies */}
                {isActive && (
                  <motion.div
                    className="absolute -inset-1 rounded-lg bg-teal-400 opacity-20"
                    animate={{
                      scale: [1, 1.1, 1],
                      opacity: [0.2, 0, 0.2]
                    }}
                    transition={{
                      duration: 2,
                      repeat: Infinity,
                      ease: "easeOut"
                    }}
                  />
                )}

                <div className="relative z-10">
                  <div className="flex items-center gap-3 mb-2">
                    <img src={tech.icon} alt={tech.name} className="w-8 h-8 object-contain" />
                    <div className="flex-1 min-w-0">
                      <div className="font-medium text-gray-900 text-sm leading-tight">
                        {tech.name}
                      </div>
                    </div>
                  </div>
                  <div className="text-xs text-gray-600">
                    {tech.description}
                  </div>
                </div>

                {/* Processing indicator */}
                {isActive && (
                  <motion.div
                    className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-teal-500 to-teal-600"
                    initial={{ scaleX: 0 }}
                    animate={{ scaleX: 1 }}
                    transition={{
                      duration: 1.5,
                      ease: "easeInOut",
                      repeat: Infinity,
                      repeatType: "reverse"
                    }}
                    style={{ transformOrigin: "left" }}
                  />
                )}
              </div>

              {/* Connection lines between active nodes */}
              {isActive && index < technologies.length - 1 && activeNodes.includes(index + 1) && (
                <motion.div
                  className="hidden md:block absolute top-1/2 -right-2 w-4 h-0.5 bg-teal-400 z-0"
                  initial={{ scaleX: 0 }}
                  animate={{ scaleX: 1 }}
                  transition={{
                    duration: 0.5,
                    delay: (index + 1) * 0.1
                  }}
                  style={{ transformOrigin: "left" }}
                />
              )}
            </motion.div>
          );
        })}
      </div>

      {/* Data flow visualization */}
      <motion.div
        className="mt-6 text-center"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1 }}
      >
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-teal-50 border border-teal-200">
          <motion.div
            className="w-2 h-2 rounded-full bg-teal-600"
            animate={{
              scale: [1, 1.5, 1],
              opacity: [1, 0.5, 1]
            }}
            transition={{
              duration: 1.5,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          />
          <span className="text-xs text-teal-700">
            Processing your documents through AI pipeline
          </span>
        </div>
      </motion.div>
    </div>
  );
}