//
// PKCS12ContainerTest.cpp
//
// Copyright (c) 2012, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "PKCS12ContainerTest.h"
#include "Poco/CppUnit/TestCaller.h"
#include "Poco/CppUnit/TestSuite.h"
#include "Poco/Crypto/EVPPKey.h"
#include "Poco/Crypto/RSAKey.h"
#include "Poco/Crypto/KeyPairImpl.h"
#include "Poco/Environment.h"
#include "Poco/Path.h"
#include "Poco/File.h"
#include "Poco/TemporaryFile.h"
#include <iostream>
#include <sstream>
#include <fstream>



using namespace Poco::Crypto;
using Poco::Environment;
using Poco::Path;
using Poco::File;
using Poco::TemporaryFile;


PKCS12ContainerTest::PKCS12ContainerTest(const std::string& name): Poco::CppUnit::TestCase(name)
{
}


PKCS12ContainerTest::~PKCS12ContainerTest()
{
}


void PKCS12ContainerTest::testFullPKCS12()
{
	try
	{
		std::string file = getTestFilesPath("full");
		full(PKCS12Container(file.c_str(), "crypto"));

		std::ifstream ifs(file.c_str(), std::ios::binary);
		PKCS12Container pkcs(ifs, "crypto");
		full(pkcs);

		PKCS12Container pkcs2(pkcs);
		full(pkcs2);

		PKCS12Container pkcs3(pkcs);
		pkcs3 = pkcs2;
		full(pkcs3);

		pkcs3 = std::move(pkcs);
		full(pkcs3);

		PKCS12Container pkcs4(std::move(pkcs2));
		full(pkcs4);
	}
	catch (Poco::Exception& ex)
	{
		std::cerr << ex.displayText() << std::endl;
		throw;
	}
}


void PKCS12ContainerTest::full(const PKCS12Container& pkcs12)
{
	assertTrue ("vally" == pkcs12.getFriendlyName());

	assertTrue (pkcs12.hasKey());
	EVPPKey pKey = pkcs12.getKey();
	assertTrue (EVP_PKEY_RSA == pKey.type());

	RSAKey rsa(pkcs12);
	assertTrue (rsa.impl()->type() == KeyPairImpl::KT_RSA_IMPL);

	assertTrue (pkcs12.hasX509Certificate());
	fullCert(pkcs12.getX509Certificate());

	std::vector<int> certOrder;
	for (int i = 0; i < 2; ++i) certOrder.push_back(i);
	fullList(pkcs12.getCACerts(), pkcs12.getFriendlyNamesCA(), certOrder);
}


void PKCS12ContainerTest::fullCert(const X509Certificate& x509)
{
	std::string subjectName(x509.subjectName());
	std::string issuerName(x509.issuerName());
	std::string commonName(x509.commonName());
	std::string country(x509.subjectName(X509Certificate::NID_COUNTRY));
	std::string localityName(x509.subjectName(X509Certificate::NID_LOCALITY_NAME));
	std::string stateOrProvince(x509.subjectName(X509Certificate::NID_STATE_OR_PROVINCE));
	std::string organizationName(x509.subjectName(X509Certificate::NID_ORGANIZATION_NAME));
	std::string organizationUnitName(x509.subjectName(X509Certificate::NID_ORGANIZATION_UNIT_NAME));
	std::string emailAddress(x509.subjectName(X509Certificate::NID_PKCS9_EMAIL_ADDRESS));
	std::string serialNumber(x509.serialNumber());

	assertTrue (subjectName == "C=CH,ST=Zug,O=Crypto Vally,CN=CV Server");
	assertTrue (issuerName == "C=CH,ST=Zug,O=Crypto Vally,CN=CV Intermediate CA v3");
	assertTrue (commonName == "CV Server");
	assertTrue (country == "CH");
	assertTrue (localityName.empty());
	assertTrue (stateOrProvince == "Zug");
	assertTrue (organizationName == "Crypto Vally");
	assertTrue (organizationUnitName.empty());
	assertTrue (emailAddress.empty());
	assertTrue (serialNumber == "1000");
	assertTrue (x509.version() == 3);
	assertTrue (x509.signatureAlgorithm() == "sha256WithRSAEncryption");
}


void PKCS12ContainerTest::fullList(const PKCS12Container::CAList& caList,
		const PKCS12Container::CANameList& caNamesList,
		const std::vector<int>& certOrder)
{
	assertTrue (certOrder.size() == caList.size());
	assertTrue ((0 == caNamesList.size()) || (certOrder.size() == caNamesList.size()));

	if (caNamesList.size())
	{
		assertTrue (caNamesList[certOrder[0]].empty());
		assertTrue (caNamesList[certOrder[1]].empty());
	}

	assertTrue (caList[certOrder[0]].subjectName() == "C=CH,ST=Zug,O=Crypto Vally,CN=CV Intermediate CA v3");
	assertTrue (caList[certOrder[0]].issuerName() == "C=CH,ST=Zug,O=Crypto Vally,CN=CV Root CA v3");
	assertTrue (caList[certOrder[0]].commonName() == "CV Intermediate CA v3");
	assertTrue (caList[certOrder[0]].subjectName(X509Certificate::NID_COUNTRY) == "CH");
	assertTrue (caList[certOrder[0]].subjectName(X509Certificate::NID_LOCALITY_NAME).empty());
	assertTrue (caList[certOrder[0]].subjectName(X509Certificate::NID_STATE_OR_PROVINCE) == "Zug");
	assertTrue (caList[certOrder[0]].subjectName(X509Certificate::NID_ORGANIZATION_NAME) == "Crypto Vally");
	assertTrue (caList[certOrder[0]].subjectName(X509Certificate::NID_ORGANIZATION_UNIT_NAME).empty());
	assertTrue (caList[certOrder[0]].subjectName(X509Certificate::NID_PKCS9_EMAIL_ADDRESS).empty());
	assertTrue (caList[certOrder[0]].serialNumber() == "1000");
	assertTrue (caList[certOrder[0]].version() == 3);
	assertTrue (caList[certOrder[0]].signatureAlgorithm() == "sha256WithRSAEncryption");

	assertTrue (caList[certOrder[1]].subjectName() == "C=CH,ST=Zug,O=Crypto Vally,CN=CV Root CA v3");
	assertTrue (caList[certOrder[1]].issuerName() == "C=CH,ST=Zug,O=Crypto Vally,CN=CV Root CA v3");
	assertTrue (caList[certOrder[1]].commonName() == "CV Root CA v3");
	assertTrue (caList[certOrder[1]].subjectName(X509Certificate::NID_COUNTRY) == "CH");
	assertTrue (caList[certOrder[1]].subjectName(X509Certificate::NID_LOCALITY_NAME).empty());
	assertTrue (caList[certOrder[1]].subjectName(X509Certificate::NID_STATE_OR_PROVINCE) == "Zug");
	assertTrue (caList[certOrder[1]].subjectName(X509Certificate::NID_ORGANIZATION_NAME) == "Crypto Vally");
	assertTrue (caList[certOrder[1]].subjectName(X509Certificate::NID_ORGANIZATION_UNIT_NAME).empty());
	assertTrue (caList[certOrder[1]].subjectName(X509Certificate::NID_PKCS9_EMAIL_ADDRESS).empty());
	assertTrue (caList[certOrder[1]].serialNumber() == "C3ECA1FCEAA16055");
	assertTrue (caList[certOrder[1]].version() == 3);
	assertTrue (caList[certOrder[1]].signatureAlgorithm() == "sha256WithRSAEncryption");
}


void PKCS12ContainerTest::testCertsOnlyPKCS12()
{
	try
	{
		std::string file = getTestFilesPath("certs-only");
		certsOnly(PKCS12Container(file.c_str(), "crypto"));

		std::ifstream ifs(file.c_str(), std::ios::binary);
		certsOnly(PKCS12Container(ifs, "crypto"));
	}
	catch (Poco::Exception& ex)
	{
		std::cerr << ex.displayText() << std::endl;
		throw;
	}
}


void PKCS12ContainerTest::certsOnly(const PKCS12Container& pkcs12)
{
	assertTrue (!pkcs12.hasKey());
	assertTrue (!pkcs12.hasX509Certificate());
	assertTrue (pkcs12.getFriendlyName().empty());

	std::vector<int> certOrder;
	for (int i = 0; i < 5; ++i) certOrder.push_back(i);
	certsOnlyList(pkcs12.getCACerts(), pkcs12.getFriendlyNamesCA(), certOrder);
}


void PKCS12ContainerTest::certsOnlyList(const PKCS12Container::CAList& caList,
	const PKCS12Container::CANameList& caNamesList, const std::vector<int>& certOrder)
{
	assertTrue (certOrder.size() == caList.size());
	assertTrue ((0 == caNamesList.size()) || (certOrder.size() == caNamesList.size()));

	if (caNamesList.size())
	{
		assertTrue (caNamesList[certOrder[0]] == "vally-ca");
		assertTrue (caNamesList[certOrder[1]] == "vally-ca");
		assertTrue (caNamesList[certOrder[2]].empty());
		assertTrue (caNamesList[certOrder[3]].empty());
		assertTrue (caNamesList[certOrder[4]].empty());
	}

	assertTrue (caList[certOrder[0]].subjectName() == "C=CH,ST=Zug,O=Crypto Vally,CN=CV Intermediate CA v3");
	assertTrue (caList[certOrder[0]].issuerName() == "C=CH,ST=Zug,O=Crypto Vally,CN=CV Root CA v3");
	assertTrue (caList[certOrder[0]].commonName() == "CV Intermediate CA v3");
	assertTrue (caList[certOrder[0]].subjectName(X509Certificate::NID_COUNTRY) == "CH");
	assertTrue (caList[certOrder[0]].subjectName(X509Certificate::NID_LOCALITY_NAME).empty());
	assertTrue (caList[certOrder[0]].subjectName(X509Certificate::NID_STATE_OR_PROVINCE) == "Zug");
	assertTrue (caList[certOrder[0]].subjectName(X509Certificate::NID_ORGANIZATION_NAME) == "Crypto Vally");
	assertTrue (caList[certOrder[0]].subjectName(X509Certificate::NID_ORGANIZATION_UNIT_NAME).empty());
	assertTrue (caList[certOrder[0]].subjectName(X509Certificate::NID_PKCS9_EMAIL_ADDRESS).empty());
	assertTrue (caList[certOrder[0]].serialNumber()== "1000");
	assertTrue (caList[certOrder[0]].version() == 3);
	assertTrue (caList[certOrder[0]].signatureAlgorithm() == "sha256WithRSAEncryption");

	assertTrue (caList[certOrder[1]].subjectName() == "C=CH,ST=Zug,O=Crypto Vally,CN=CV Root CA v3");
	assertTrue (caList[certOrder[1]].issuerName() == "C=CH,ST=Zug,O=Crypto Vally,CN=CV Root CA v3");
	assertTrue (caList[certOrder[1]].commonName() == "CV Root CA v3");
	assertTrue (caList[certOrder[1]].subjectName(X509Certificate::NID_COUNTRY) == "CH");
	assertTrue (caList[certOrder[1]].subjectName(X509Certificate::NID_LOCALITY_NAME).empty());
	assertTrue (caList[certOrder[1]].subjectName(X509Certificate::NID_STATE_OR_PROVINCE) == "Zug");
	assertTrue (caList[certOrder[1]].subjectName(X509Certificate::NID_ORGANIZATION_NAME) == "Crypto Vally");
	assertTrue (caList[certOrder[1]].subjectName(X509Certificate::NID_ORGANIZATION_UNIT_NAME).empty());
	assertTrue (caList[certOrder[1]].subjectName(X509Certificate::NID_PKCS9_EMAIL_ADDRESS).empty());
	assertTrue (caList[certOrder[1]].serialNumber() == "C3ECA1FCEAA16055");
	assertTrue (caList[certOrder[1]].version() == 3);
	assertTrue (caList[certOrder[1]].signatureAlgorithm() == "sha256WithRSAEncryption");

	assertTrue (caList[certOrder[2]].subjectName() == "C=US,O=Internet Security Research Group,CN=ISRG Root X1");
	assertTrue (caList[certOrder[2]].issuerName() == "C=US,O=Internet Security Research Group,CN=ISRG Root X1");
	assertTrue (caList[certOrder[2]].commonName() == "ISRG Root X1");
	assertTrue (caList[certOrder[2]].subjectName(X509Certificate::NID_COUNTRY) == "US");
	assertTrue (caList[certOrder[2]].subjectName(X509Certificate::NID_LOCALITY_NAME).empty());
	assertTrue (caList[certOrder[2]].subjectName(X509Certificate::NID_STATE_OR_PROVINCE).empty());
	assertTrue (caList[certOrder[2]].subjectName(X509Certificate::NID_ORGANIZATION_NAME) == "Internet Security Research Group");
	assertTrue (caList[certOrder[2]].subjectName(X509Certificate::NID_ORGANIZATION_UNIT_NAME).empty());
	assertTrue (caList[certOrder[2]].subjectName(X509Certificate::NID_PKCS9_EMAIL_ADDRESS).empty());
	assertTrue (caList[certOrder[2]].serialNumber() == "8210CFB0D240E3594463E0BB63828B00");
	assertTrue (caList[certOrder[2]].version() == 3);
	assertTrue (caList[certOrder[2]].signatureAlgorithm() == "sha256WithRSAEncryption");

	assertTrue (caList[certOrder[3]].subjectName() == "C=US,O=Let's Encrypt,CN=Let's Encrypt Authority X3");
	assertTrue (caList[certOrder[3]].issuerName() == "O=Digital Signature Trust Co.,CN=DST Root CA X3");
	assertTrue (caList[certOrder[3]].commonName() == "Let's Encrypt Authority X3");
	assertTrue (caList[certOrder[3]].subjectName(X509Certificate::NID_COUNTRY) == "US");
	assertTrue (caList[certOrder[3]].subjectName(X509Certificate::NID_LOCALITY_NAME).empty());
	assertTrue (caList[certOrder[3]].subjectName(X509Certificate::NID_STATE_OR_PROVINCE).empty());
	assertTrue (caList[certOrder[3]].subjectName(X509Certificate::NID_ORGANIZATION_NAME) == "Let's Encrypt");
	assertTrue (caList[certOrder[3]].subjectName(X509Certificate::NID_ORGANIZATION_UNIT_NAME).empty());
	assertTrue (caList[certOrder[3]].subjectName(X509Certificate::NID_PKCS9_EMAIL_ADDRESS).empty());
	assertTrue (caList[certOrder[3]].serialNumber() == "0A0141420000015385736A0B85ECA708");
	assertTrue (caList[certOrder[3]].version() == 3);
	assertTrue (caList[certOrder[3]].signatureAlgorithm() == "sha256WithRSAEncryption");

	assertTrue (caList[certOrder[4]].subjectName() == "C=US,O=Let's Encrypt,CN=Let's Encrypt Authority X3");
	assertTrue (caList[certOrder[4]].issuerName() == "C=US,O=Internet Security Research Group,CN=ISRG Root X1");
	assertTrue (caList[certOrder[4]].commonName() == "Let's Encrypt Authority X3");
	assertTrue (caList[certOrder[4]].subjectName(X509Certificate::NID_COUNTRY) == "US");
	assertTrue (caList[certOrder[4]].subjectName(X509Certificate::NID_LOCALITY_NAME).empty());
	assertTrue (caList[certOrder[4]].subjectName(X509Certificate::NID_STATE_OR_PROVINCE).empty());
	assertTrue (caList[certOrder[4]].subjectName(X509Certificate::NID_ORGANIZATION_NAME) == "Let's Encrypt");
	assertTrue (caList[certOrder[4]].subjectName(X509Certificate::NID_ORGANIZATION_UNIT_NAME).empty());
	assertTrue (caList[certOrder[4]].subjectName(X509Certificate::NID_PKCS9_EMAIL_ADDRESS).empty());
	assertTrue (caList[certOrder[4]].serialNumber() == "D3B17226342332DCF40528512AEC9C6A");
	assertTrue (caList[certOrder[4]].version() == 3);
	assertTrue (caList[certOrder[4]].signatureAlgorithm() == "sha256WithRSAEncryption");

}


void PKCS12ContainerTest::testPEMReadWrite()
{
	try
	{
		std::string file = getTestFilesPath("certs-only", "pem");
		X509Certificate::List certsOnly = X509Certificate::readPEM(file);
		assertTrue (certsOnly.size() == 5);
		std::vector<int> certOrder;
		for(int i = 0; i < certsOnly.size(); ++i) certOrder.push_back(i);
		certsOnlyList(certsOnly, PKCS12Container::CANameList(), certOrder);

		TemporaryFile tmpFile;
		X509Certificate::writePEM(tmpFile.path(), certsOnly);

		certsOnly.clear();
		certsOnly = X509Certificate::readPEM(tmpFile.path());
		certsOnlyList(certsOnly, PKCS12Container::CANameList(), certOrder);

		file = getTestFilesPath("full", "pem");
		X509Certificate::List full = X509Certificate::readPEM(file);
		assertTrue (full.size() == 3);
		fullCert(full[0]);
		full.erase(full.begin());
		assertTrue (full.size() == 2);

		certOrder.clear();
		for(int i = 0; i < full.size(); ++i) certOrder.push_back(i);
		fullList(full, PKCS12Container::CANameList(), certOrder);

		TemporaryFile tmpFile2;
		X509Certificate::writePEM(tmpFile2.path(), full);

		full.clear();
		full = X509Certificate::readPEM(tmpFile2.path());
		fullList(full, PKCS12Container::CANameList(), certOrder);
	}
	catch (Poco::Exception& ex)
	{
		std::cerr << ex.displayText() << std::endl;
		throw;
	}
}


void PKCS12ContainerTest::setUp()
{
}


void PKCS12ContainerTest::tearDown()
{
}


std::string PKCS12ContainerTest::getTestFilesPath(const std::string& name, const std::string& ext)
{
	std::ostringstream ostr;
	ostr << "data/" << name << '.' << ext;
	std::string fileName(ostr.str());
	Poco::Path path(fileName);
	if (Poco::File(path).exists())
	{
		return fileName;
	}

	ostr.str("");
	ostr << "/Crypto/testsuite/data/" << name << '.' << ext;
	fileName = Poco::Environment::get("POCO_BASE") + ostr.str();
	path = fileName;

	if (!Poco::File(path).exists())
	{
		std::cerr << "Can't find " << fileName << std::endl;
		throw Poco::NotFoundException("cannot locate directory containing valid Crypto test files");
	}
	return fileName;
}


Poco::CppUnit::Test* PKCS12ContainerTest::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("PKCS12ContainerTest");

	CppUnit_addTest(pSuite, PKCS12ContainerTest, testFullPKCS12);
	CppUnit_addTest(pSuite, PKCS12ContainerTest, testCertsOnlyPKCS12);
	CppUnit_addTest(pSuite, PKCS12ContainerTest, testPEMReadWrite);

	return pSuite;
}
