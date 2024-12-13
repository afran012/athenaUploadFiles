import pytest
from unittest.mock import Mock, patch
from spatial_migration.core.extractor import PostgreSQLExtractor

def test_extract_table(sample_config, sample_geodataframe):
    """Prueba la extracción de datos desde PostgreSQL"""
    with patch('geopandas.read_postgis') as mock_read_postgis:
        mock_read_postgis.return_value = sample_geodataframe
        
        extractor = PostgreSQLExtractor(sample_config.postgres)
        result = extractor.extract_table('test_table')
        
        assert len(result) == len(sample_geodataframe)
        assert all(result.columns == sample_geodataframe.columns)

def test_extract_table_with_where_clause(sample_config):
    """Prueba la extracción con cláusula WHERE"""
    with patch('geopandas.read_postgis') as mock_read_postgis:
        extractor = PostgreSQLExtractor(sample_config.postgres)
        extractor.extract_table('test_table', where_clause="id = 1")
        
        # Verificar que la consulta incluye la cláusula WHERE
        call_args = mock_read_postgis.call_args[0]
        assert "WHERE id = 1" in call_args[0]