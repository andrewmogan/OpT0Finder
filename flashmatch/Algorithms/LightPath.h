/**
 * \file LightPath.h
 *
 * \ingroup Algorithms
 *
 * \brief Class def header for a class LightPath
 *
 * @author Rui
 */

/** \addtogroup Algorithms

    @{*/
#ifndef LightPath_H
#define LightPath_H

#include <iostream>
#include <numeric>
#include <functional>
#include <algorithm>

#include "flashmatch/GeoAlgo/GeoTrajectory.h"
#include "flashmatch/Base/BaseAlgorithm.h"
#include "flashmatch/Base/CustomAlgoFactory.h"

namespace flashmatch{
/**
   \class LightPath
   User defined class LightPath ... these comments are used to generate
   doxygen documentation!
 */

  class LightPath : public flashmatch::BaseAlgorithm {

  public:

    /// Default constructor
    LightPath(const std::string name="LightPath");

    /// Default destructor
    ~LightPath(){}

    // Setter function
    double Set_Gap      ( double x) { _gap   =x;      return _gap;}

    // Flash Hypothesis for Trajectory (Track)
    flashmatch::QCluster_t MakeQCluster(const ::geoalgo::Trajectory& trj) const;

    void MakeQCluster(const ::geoalgo::Vector& pt_1,
		      const ::geoalgo::Vector& pt_2,
		      flashmatch::QCluster_t& Q_cluster,
		      double dedx=-1) const;

    // Getter for light yield configured paramater
    double GetLightYield() const { return _light_yield; }

  protected:

    void _Configure_(const Config_t &pset);

    double _gap;
    double _light_yield;
    double _dEdxMIP;
  };

  /**
     \class flashmatch::LightPathFactory
  */
  class LightPathFactory : public CustomAlgoFactoryBase {
  public:
    /// ctor
    LightPathFactory() { CustomAlgoFactory::get().add_factory("LightPath",this); }
    /// dtor
    ~LightPathFactory() {}
    /// creation method
    BaseAlgorithm* create(const std::string instance_name) { return new LightPath(instance_name); }
  };
}

#endif
/** @} */ // end of doxygen group
